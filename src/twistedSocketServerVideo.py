from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet import reactor
import sys
#import leveldb

# TODO: Create socket server class and protocol @Pontus

## make sure videofeed keeps a list of videofeed observers so it can update several in one go.

class CasperProtocol(DatagramProtocol):
    def __init__(self):
        print 'new protocol instance'

    def startProtocol(self):
        "Called when transport is connected"
        pass

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

        self.transport.write(data, (host, port))

class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'

    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

Port = int(sys.argv[1])

reactor.listenMulticast(Port, CasperProtocol())
print 'server started on', Port
reactor.run()
