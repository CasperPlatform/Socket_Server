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

    def startProtocol(self):
        "Called when transport is connected"
        self.connected = True
        pass
    def stopProtocol(self):
        self.connected = False
        pass
    def outputs(self, data, (host, port)):
        stream = io.BytesIO()
        for i in range(20):
            # This returns the stream for the camera to capture to
            yield stream

            stream.seek(0)
            b = stream.read()

            packetLen = 512
            packets = int(math.ceil(len(b)/512.0))

            message = "V" + str(packets)
            print message
            self.transport.write(message, (host, port))
            print "%f, %d" % (len(b)/512.0, packets)

            for i in range(0, packets):

                if i==packets-1:
                    message = b[packetLen*i:]
                    self.transport.write(message, (host, port))

                else:
                    message = b[packetLen*i:packetLen*(i+1)]
                    self.transport.write(message, (host, port))

            stream.seek(0)
            stream.truncate()

    def datagramReceived(self, data, (host, port)):

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 40
            time.sleep(2)

            while True:

                if self.connected == False:
                    break

                start = time.time()
                camera.capture_sequence(self.outputs(data, (host, port)), 'jpeg', use_video_port=True)
                finish = time.time()
                print('Captured 20 images at %.2ffps' % (20 / (finish - start)))




class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'

    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

Port = int(sys.argv[1])

reactor.listenMulticast(Port, CasperProtocol())
print 'server started on', Port
reactor.run()
