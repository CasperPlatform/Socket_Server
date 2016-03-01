from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import sys
import serial

class CasperProtocol(Protocol):
    def __init__(self,clients):
        print 'new protocol instance'
        self.clients = clients

    def connectionMade(self):
        self.clients.append(self)
        print 'A client has connected'
        print "clients are ", self.clients
    def connectionLost(self, reason):
        self.clients.remove(self)
        print 'A client disconnected'
        print "clients are ", self.clients
    def dataReceived(self, data):
        len = 4
        tmp = ''
        datarec = bytearray()
        for byte in data:

            datarec.append(ord(byte))
            if hex(ord(byte)) == '0xd':
                tmp = byte
                continue
            if tmp != '':
                if hex(ord(byte)) == '0xa' and hex(ord(tmp)) == '0xd':
                    print 'got CLRF'
                    break
        for byte in datarec:
            print repr(byte),' '
            


class SmartcarFactory(Factory):
    def __init__(self):
        print 'initing'
        self.tokens={}
        self.clients = []
    def buildProtocol(self, addr):
        return CasperProtocol(self.clients)

print sys.byteorder
Port = int(sys.argv[1])
# factory = Factory()
# factory.clients = []
# factory.protocol = CasperProtocol
reactor.listenTCP(Port,SmartcarFactory())
print 'server started on', Port
reactor.run()
