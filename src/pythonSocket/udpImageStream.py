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

    while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(4096)

        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >>sys.stderr, data
        time.sleep(0.1)
        #global continueSending
        #print continueSending
        if data:
            #continueSending = True

            thr = threading.Thread(target=sendImage, args=(sock, data, address), kwargs={})
            thr.start() # will run "foo"

        #else:
            #continueSending = False
def sendImage(sock, data, address):

    imageNumber = 0
    global continueSending

    with picamera.PiCamera() as camera:
        imageNumber = 283928391
        stream = io.BytesIO()
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(stream, 'jpeg')
        print "received %r." % (data)

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
    #print message
    sent = sock.sendto(message, address)
    #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)

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
            sent = sock.sendto(message, address)
            #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
        else:
            message.extend(b[packetLen*i:packetLen*(i+1)])
            sent = sock.sendto(message, address)
            #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
        #print 'packet ' + str(i) + ' sent.'
        #imageNumber += 1
        #print 'Sent image number: ' + str(imageNumber)
        #time.sleep(0.002)
        
if __name__ == '__main__':
    listen()
