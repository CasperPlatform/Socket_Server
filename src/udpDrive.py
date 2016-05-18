
import socket
import sys
import serial
import threading
import math
import io
import time
import sqlite3
import datetime

from enum import Enum

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

localToken = None

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global port
    port = int(sys.argv[1])
    # Bind the socket to the port
    server_address = ('', port)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)

        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >>sys.stderr, repr(data)

        if data:
            readMessage(data, sock, address)

def sendCmd(cmd):
    global port
    ser = serial.Serial(port, 9600)

    for byte in cmd:
        ser.write(chr(byte))


def readMessage(message, sock, address):

    print ord(message[0])
    if not ord(message[0]) == 0x01:
        print 'Wrong message header.'
        return

    token = message[1:17]

    if token !=  self.localToken[0] or  self.localToken[1] - datetime.datetime.now() < datetime.timedelta(minutes = 5):
        print "Open DB"
        conn = sqlite3.connect('/home/pi/CASPER/db.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("select token, expiration from tokens where token=? and expiration>?", (token, datetime.datetime.now()))

        row = c.fetchone()
        print row
        if row is None:
            print 'No token found.'
            return
        else:
            localToken = row

        c.execute("update tokens set expiration=? where userId=?", (datetime.datetime.now() + datetime.timedelta(minutes = 25), row[0]))
        conn.commit()

    flag = message[17]

    # message parsing
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
                print 'got CL,LF,EOF'
                break

    if datarec[0] != ord(typeFlag.Drive):
         print repr(datarec[0])
         print 'unknown typeFlag...aborting'
         return
    else:
        tf = typeFlag.Drive
        print 'this is a driveMsg'

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

    cmd = bytearray()
    cmd.append(message[0])
    cmd.extend(message[17:24])
    print repr(cmd)
    sendCmd(cmd)
