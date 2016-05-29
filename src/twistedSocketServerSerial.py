#!/usr/bin/python

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

import sys
import serial
import sqlite3
import datetime
#import leveldb

from enum import Enum


## make sure videofeed keeps a list of videofeed observers so it can update several in one


class typeFlag(Enum):
    Drive = 'D'
class directionFlag(Enum):
    Forward  = 'F'
    Backward = 'B'
    Idle     = 'I'
class angleFlag(Enum):
    Right = 'R'
    Left  = 'L'
    Idle  = 'I'

serServ = None

class USBclient(Protocol):
    def connectionMade(self):
        global serServ
        serServ = self
        #serServ.transport.write()
        print 'Arduino device: ', serServ, ' is connected.'

    def cmdReceived(self, cmd):
        #serServ.transport.write(cmd)
        for byte in cmd:
            serServ.transport.write(chr(byte))
        #leaving all newlines for debug reasons
        #print cmd, ' - sent to Arduino.'

    def dataReceived(self,data):
        print 'USBclient.dataReceived called with:'
        print data

class CasperProtocol(Protocol):

    localToken = None

    def __init__(self,clients):
        print 'new protocol instance'
        self.clients = clients
        self.localToken = (None,datetime.datetime.now)
        # get db instance
        #self.level = leveldb.LevelDB('path')

    def connectionMade(self):
        self.clients.append(self)
        print 'A client has connected'
        print "clients are ", self.clients
    def connectionLost(self, reason):
        self.clients.remove(self)
        print 'A client disconnected'
        print "clients are ", self.clients
    def dataReceived(self, data):
        myArduino = USBclient()
        CR    =  ''
        LF    =  ''
        tf    = typeFlag.Drive
        df    = directionFlag.Forward
        af    = angleFlag.Right
        speed = 0
        angle = 0

        datarec = bytearray()
        for byte in data:
            datarec.append(ord(byte))
            if hex(ord(byte)) == '0xd':
                CR = byte
                continue
            if hex(ord(byte)) == '0xa':
                LF = byte
                continue
            if CR != '' and LF != '':
                if hex(ord(byte)) == '0x4' and hex(ord(CR)) == '0xd' and hex(ord(LF)) == '0xa':
                    print 'got CL,RF,EOF'
                    break

        # We no have a Message! A good starting point would be to verify the user token.

        if datarec[0] != ord(typeFlag.Drive):
             print repr(datarec[0])
             print 'unknown typeFlag...aborting'
             return
        else:
            tf = typeFlag.Drive
            print 'this is a driveMsg'


        token = str(datarec[1:17])

        print repr(token)
        print repr(self.localToken)

        if False and token !=  self.localToken[0] or  self.localToken[1] - datetime.datetime.now() < datetime.timedelta(minutes = 5):
            print "Open DB"
            conn = sqlite3.connect('/home/pi/db.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute("select token, expiration from tokens where token=? and expiration>?", (token, datetime.datetime.now()))

            row = c.fetchone()
            print row
            if row is None:
                print 'No token found.'
                #return
            else:
                self.localToken = row

            c.execute("update tokens set expiration=? where userId=?", (datetime.datetime.now() + datetime.timedelta(minutes = 25), row[0]))
            conn.commit()


        if datarec[17] == ord(directionFlag.Forward) or datarec[17] == ord(directionFlag.Backward) or datarec[17] == ord(directionFlag.Idle):
            if datarec[17] == ord(directionFlag.Forward):
                print 'direction: Forward'
                df = directionFlag.Forward
            if datarec[17] == ord(directionFlag.Backward):
                print 'direction: Back'
                df = directionFlag.Backward
            if datarec[17] == ord(directionFlag.Idle):
                print 'direction: Idle'
                df = directionFlag.Idle
        else:
            print 'unknown DirectionFlag..aborting'
            return
        if datarec[18] == ord(angleFlag.Right) or datarec[18] == ord(angleFlag.Left) or datarec[18] == ord(angleFlag.Idle):
            if datarec[18] == ord(angleFlag.Right):
                print 'angle: Right'
                df = angleFlag.Right
            if datarec[18] == ord(angleFlag.Left):
                print 'angle: Left'
                df = angleFlag.Left
            if datarec[18] == ord(angleFlag.Idle):
                print 'angle: Idle'
                df = angleFlag.Idle
        else:
            print 'unknown AngleFlag..aborting'
            for i,byte in enumerate(datarec):
                print repr(byte),' '
            return
        if datarec[19] < 0 or datarec[19] > 255:
            print 'invalid Speed Value, aborting...'
            return
        else:
            speed = datarec[19]
            print 'speed : ',speed
        if datarec[20] < 0 or datarec[20] > 90:
            print 'invalid Angle Value, aborting...'
            return
        else:
            angle = datarec[20]
            print 'angle : ',angle

        print 'successfully parsed buffer!, sending to serial'

        message = bytearray()
        message.append(datarec[0])
        message.extend(datarec[17:24])
        print repr(message)
        myArduino.cmdReceived(message)
        #
        # for i,byte in enumerate(datarec):
        #     print repr(byte),' '




class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'
        self.tokens={}
        self.clients = []
    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

print sys.byteorder
Port = int(sys.argv[1])
# factory = Factory()
# factory.clients = []
# factory.protocol = CasperProtocol
reactor.listenTCP(Port,SmartcarFactory())
SerialPort(USBclient(), '/dev/ttyACM0', reactor, baudrate='9600')
print 'server started on', Port
reactor.run()
