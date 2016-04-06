import socket
import sys
import threading
import math
import io
import time
import picamera

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
        print >>sys.stderr, data

        if not continueSending:
            continueSending = True

            thr = threading.Thread(target=startVideo, args=(sock, data, address), kwargs={})
            thr.start() # will run "foo"

        else:
            continueSending = False

def outputs(sock, data, address):
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

def startVideo(sock, data, address):

    global imageNumber
    imageNumber = 0
    global continueSending

    with picamera.PiCamera() as camera:
        camera.resolution = (334, 188)
        camera.framerate = 40
        time.sleep(2)

        while continueSending:

            start = time.time()

            camera.capture_sequence(outputs(sock, data, address), 'jpeg', use_video_port=True)

            finish = time.time()
            print('Captured 20 images at %.2ffps' % (20 / (finish - start)))

if __name__ == '__main__':
    listen()
