
import socket
import sys
import serial
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

localToken = (None, None)

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
    sPort = '/dev/ttyACM0'
    ser = serial.Serial(sPort, 9600)

    for byte in cmd:
        ser.write(chr(byte))


def readMessage(message, sock, address):
    global localToken

    print ord(message[0])
    if not ord(message[0]) == 0x01:
        print 'Wrong message header.'
        return

    token = message[1:17]

    if token !=  localToken[0] or  localToken[1] - datetime.datetime.now() < datetime.timedelta(minutes = 5):
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
    CR    =  ''
    LF    =  ''
    tf    = typeFlag.Camera
    xf    = xFlag.Idle
    yf    = yFlag.Idle
    xAngle = 0
    yAngle = 0

    datarec = bytearray()
    for byte in message:
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

    if datarec[17] != ord(typeFlag.Camera):
         print repr(datarec[17])
         print 'unknown typeFlag...aborting'
         return
    else:
        tf = typeFlag.Camera
        print 'this is a cameraMsg'

    if datarec[18] == ord(xFlag.Right) or datarec[18] == ord(xFlag.Left) or datarec[18] == ord(xFlag.Idle):
        if datarec[18] == ord(xFlag.Right):
            print 'x: Right'
            df = xFlag.Right
        if datarec[18] == ord(xFlag.Left):
            print 'x: Left'
            df = xFlag.Left
        if datarec[18] == ord(xFlag.Idle):
            print 'x: Idle'
            df = xFlag.Idle
    else:
        print 'unknown xFlag..aborting'
        return

    if datarec[19] < 0 or datarec[19] > 90:
        print 'invalid xAngle Value, aborting...'
        return
    else:
        xAngle = datarec[19]
        print 'xAngle : ',xAngle

    if datarec[20] == ord(yFlag.Right) or datarec[20] == ord(yFlag.Left) or datarec[20] == ord(yFlag.Idle):
        if datarec[20] == ord(yFlag.Up):
            print 'y: Up'
            df = yFlag.Up
        if datarec[20] == ord(yFlag.Down):
            print 'y: Down'
            df = yFlag.Down
        if datarec[20] == ord(yFlag.Idle):
            print 'y: Idle'
            df = yFlag.Idle
    else:
        print 'unknown yFlag..aborting'
        for i,byte in enumerate(datarec):
            print repr(byte),' '
        return

    if datarec[21] < 0 or datarec[21] > 90:
        print 'invalid Angle Value, aborting...'
        return
    else:
        angle = datarec[21]
        print 'yAngle : ',yAngle

    print 'successfully parsed buffer!, sending to serial'

    cmd = bytearray()
    cmd.append(message[17:24])
    print repr(cmd)
    sendCmd(cmd)

if __name__ == '__main__':
    listen()
