from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet import reactor
import sys
import math
import io
import time
import picamera

#import leveldb

# TODO: Create socket server class and protocol @Pontus

## make sure videofeed keeps a list of videofeed observers so it can update several in one go.

class CasperProtocol(DatagramProtocol):

    def __init__(self):
        print 'new protocol instance'

    def connectionLost(self, reason):
        self.clients.remove(self)
        print 'A client disconnected'
        print "clients are ", self.clients
        self.connected = false

    def startProtocol(self):
        "Called when transport is connected"
        self.connected = True
        pass

    def stopProtocol(self):
        self.connected = False
        pass

    def datagramReceived(self, data, (host, port)):

        with picamera.PiCamera() as camera:
            imageNumber = 283928391
            stream = io.BytesIO()
            camera.start_preview()
            # Camera warm-up time
            time.sleep(2)
            camera.capture(stream, 'jpeg')
            print "received %r from %s:%d" % (data, host, port)

            stream.seek(0)
            b = stream.read()
            print len(b)
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

            print message
            self.transport.write(message, (host, port))

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
                    self.transport.write(message, (host, port))

                else:
                    message.extend(b[packetLen*i:packetLen*(i+1)])
                    self.transport.write(message, (host, port))
                print 'packet ' + str(i) + ' sent.'
                time.sleep(0.02)

class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'

    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

Port = int(sys.argv[1])

reactor.listenMulticast(Port, CasperProtocol())
print 'server started on', Port
reactor.run()
