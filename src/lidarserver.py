import socket
import sys
import threading
import time
import sqlite3
import datetime
import serial
import math
import enum

class directionFlag(Enum):
    Forward  = 'F'
    Backward = 'B'
    Idle     = 'I'

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 9998
    # Bind the socket to the port
    server_address = ('', port)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    global continueSending
    continueSending = False

    while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)

        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >>sys.stderr, repr(data)

        if data:
            readMessage(data, sock, address)
            
def readMessage(message, sock, address):
    global continueSending
    global timer

    if not message[0] == 'L':
        print 'Wrong message header.'
        return
    
    #token = message[1:17]

    #conn = sqlite3.connect('/home/pi/CASPER/db.db', detect_types=sqlite3.PARSE_DECLTYPES)
    #c = conn.cursor()

    #c.execute("select userId from tokens where token=? and expiration>?", (token, datetime.datetime.now()))
    #c.execute("select * from tokens where token=? and expiration>?", (token, datetime.datetime.now()))

    #row = c.fetchone()
    #print row
    #if row is None:
     #   print 'No token found.'
     #   return

    #c.execute("update tokens set expiration=? where userId=?", (datetime.datetime.now() + datetime.timedelta(minutes = 25), row[0]))
    #conn.commit()

    flag = message[17]
    global direction
    
    if flag == 'S':
        continueSending = True

        thr1 = threading.Thread(target=startMeasure, args=(sock, address), kwargs={})
        thr1.start()

        thr2 = threading.Thread(target=videoTimer, args=(), kwargs={})
        thr2.start()

        print 'Start Sending Lidar Data.'

    elif flag == 'F':
        direction = directionFlag.Forward
        timer = 0

    elif flag == 'B':
        direction = directionFlag.Backward
        timer = 0

    elif flag == 'I':
        direction = directionFlag.Idle
        timer = 0

    elif flag == 's':
        continueSending = False
        timer = 0
        print 'Stop Sending Lidar Data.'
        
def startMeasure(sock, address):

    global continueSending
    
    while continueSending:
        
        message = bytearray()
        
        message.append(0x01)
        message.append('L')
        
        for i in range (0, 360):
            point = addPoint(i, 500)
            
            message.append((point[0]>>8) & 0xff)
            message.append(point[0] & 0xff)
            
            message.append((point[1]>>8) & 0xff)
            message.append(point[1] & 0xff)
            
        
        sock.sendto(message, address)
        time.sleep(1)
        
def addPoint(angle, distance):

    x = 250
    y = 250
    
    if angle == 0 or angle == 360:
        x += 0
        y -= distance
        firstPoint = True
        lastPoint = (x, y)
    elif angle < 90:
        radian = math.radians(angle)

        x += math.sin(radian)*distance
        y -= math.cos(radian)*distance
    elif angle == 90:
        x += distance
    elif angle < 180:
        radian = math.radians(angle-90)

        x += math.cos(radian)*distance
        y += math.sin(radian)*distance
    elif angle == 180:
        y += distance
    elif angle < 270:
        radian = math.radians(angle-180)

        x -= math.sin(radian)*distance
        y += math.cos(radian)*distance
    elif angle == 270:
        x -= distance
    elif angle < 360:
        radian = math.radians(angle-270)

        x -= math.cos(radian)*distance
        y -= math.sin(radian)*distance

    return (int(x), int(y))
    
def videoTimer():
    global timer
    global continueSending
    timer = 0
    while timer < 10:
        timer += 1
        time.sleep(1)

    continueSending = False
    
if __name__ == '__main__':
    listen()
