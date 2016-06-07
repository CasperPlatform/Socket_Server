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
    Camera = 'C'
class YFlag(Enum):
    Upward  = 'U'
    Downward = 'D'
    Idle     = 'I'
class XFlag(Enum):
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
        print "clients are ", self.clents
    def dataReceived(self, data):
        myArduino = USBclient()
        CR    =  ''
        LF    =  ''
        tf    = typeFlag.Camera
        df    = XFlag.Right
        af    = YFLAG.Upward
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

        if datarec[0] != ord(typeFlag.Camera):
             print repr(datarec[0])
             print 'unknown typeFlag...aborting'
             return
        else:
            tf = typeFlag.Camera
            print 'this is a cameraMsg'

        if datarec[1] == ord(XFlag.Right) or datarec[1] == ord(XFlag.Left) or datarec[1] == ord(XFlag.Idle):
            if datarec[1] == ord(dXFlag.Right):
                print 'direction: Right'
                df = XFlag.Right
            if datarec[1] == ord(XFlag.Left):
                print 'direction: Left'
                df = XFlag.Left
            if datarec[1] == ord(XFlag.Idle):
                print 'direction: Idle'
                df = XFlag.Idle
        else:
            print 'unknown DirectionFlag..aborting'
            return
        if datarec[3] == ord(YFlag.Upward) or datarec[3] == ord(YFlag.Downward) or datarec[3] == ord(YFlag.Idle):
            if datarec[3] == ord(YFlag.Upward):
                print 'Y: Upward'
                df = YFlag.Upward
            if datarec[3] == ord(YFlag.Downward):
                print 'Y: Downward'
                df = YFlag.Downward
            if datarec[3] == ord(YFlag.Idle):
                print 'Y: Idle'
                df = YFlag.Idle
        else:
            print 'unknown AngleFlag..aborting'
            for i,byte in enumerate(datarec):
                print repr(byte),' '
            return
        if datarec[2] < 0 or datarec[2] > 90:
            print 'invalid X Value, aborting...'
            return
        else:
            X = datarec[2]
            print 'X : ',X
        if datarec[4] < 0 or datarec[4] > 90:
            print 'invalid Y Value, aborting...'
            return
        else:
            Y = datarec[4]
            print 'Y : ',Y

        print 'successfully parsed buffer!, sending to serial'

        print repr(datarec)
        myArduino.cmdReceived(datarec)
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
