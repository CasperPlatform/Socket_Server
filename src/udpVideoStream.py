#!/usr/bin/python

import socket
import sys
import threading
import math
import io
import time
import picamera
import sqlite3
import datetime

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(sys.argv[1])
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

    print ord(message[0])
    if not ord(message[0]) == 0x01:
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

    if flag == 'S':
        continueSending = True

        thr1 = threading.Thread(target=startVideo, args=(sock, address), kwargs={})
        thr1.start()

        thr2 = threading.Thread(target=videoTimer, args=(), kwargs={})
        thr2.start()

        print 'Start Sending Video.'

    if flag == 's':
        continueSending = False
        timer = 0
        print 'Stop Sending Video.'

    if flag == 'I':
        timer = 0
        print 'Recieved Idle Update.'

def outputs(sock, address):
      stream = io.BytesIO()

      global continueSending
      global imageNumber

      for i in range(20):
          # This returns the stream for the camera to capture to
          if not continueSending:
              break

          yield stream
          imageNumber += 1
          stream.seek(0)
          b = stream.read()

          packetLen = 8000
          packets = int(math.ceil(len(b)/8000.0))

          message = bytearray()
          message.append(0x01)
          message.append('V')

          message.append((imageNumber>>24) & 0xff)
          message.append((imageNumber>>16) & 0xff)
          message.append((imageNumber>>8) & 0xff)
          message.append(imageNumber & 0xff)

          message.append(packets)

          length = len(b)
          message.append((length>>24) & 0xff)
          message.append((length>>16) & 0xff)
          message.append((length>>8) & 0xff)
          message.append(length & 0xff)

          #print repr(message)
          sock.sendto(message, address)
          #print "%f, %d" % (len(b)/8000.0, packets)

          for i in range(0, packets):

              message = bytearray()
              message.append(0x02)

              message.append((imageNumber>>24) & 0xff)
              message.append((imageNumber>>16) & 0xff)
              message.append((imageNumber>>8) & 0xff)
              message.append(imageNumber & 0xff)

              message.append(i)

              if i==packets-1:
                  message.extend(b[packetLen*i:])
                  sock.sendto(message, address)

              else:
                  message.extend(b[packetLen*i:packetLen*(i+1)])
                  sock.sendto(message, address)
              #print 'packet ' + str(i) + ' sent.'
              #time.sleep(0.001)

          stream.seek(0)
          stream.truncate()

def startVideo(sock, address):

    global imageNumber
    imageNumber = 0
    global continueSending

    with picamera.PiCamera() as camera:
        camera.resolution = (334, 188)
        camera.framerate = 40
        time.sleep(2)

        while continueSending:

            start = time.time()

            camera.capture_sequence(outputs(sock, address), 'jpeg', use_video_port=True)

            finish = time.time()
            print('Captured 20 images at %.2ffps' % (20 / (finish - start)))

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
