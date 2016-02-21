from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import sys

class casperProtocol(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print 'A client has connected'
        print "clients are ", self.factory.clients
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print 'A client disconnected'
        print "clients are ", self.factory.clients
    def dataReceived(self, data):
        for byte in data:
            print repr(byte)
            if hex(int(repr(byte))) == 0x04:
                print 'end of message'

print sys.byteorder
Port = int(sys.argv[1])
factory = Factory()
factory.clients = []
factory.protocol = casperProtocol
reactor.listenTCP(Port,factory)
print 'server started on', Port
reactor.run()
