from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet import reactor
import sys
import math
import io
import time

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

        with open("img.jpg", "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)
        print "received %r from %s:%d" % (data, host, port)

        packetLen = 8000
        packets = int(math.ceil(len(b)/8000.0))

        message = "V" + str(packets) + str(len(b))
        print message
        self.transport.write(message, (host, port))

        for i in range(0, packets):

            if i==packets-1:
                message = b[packetLen*i:]
                self.transport.write(message, (host, port))

            else:
                message = b[packetLen*i:packetLen*(i+1)]
                self.transport.write(message, (host, port))
            print 'packet ' + str(i) + ' sent.'

class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'

    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

Port = int(sys.argv[1])

reactor.listenMulticast(Port, CasperProtocol())
print 'server started on', Port
reactor.run()
