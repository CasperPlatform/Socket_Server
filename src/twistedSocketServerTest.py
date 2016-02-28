from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
import sys
import serial

serServ = None

class USBclient(Protocol):
    def connectionMade(self):
        global serServ
        serServ = self
        print 'Arduino device: ', serServ, ' is connected.'

    def cmdReceived(self, cmd):
        serServ.transport.write(cmd)
        #leaving all newlines for debug reasons
        print cmd, ' - sent to Arduino.'
        pass

    def dataReceived(self,data):
        print 'USBclient.dataReceived called with:'
        print str(data)

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

        myArduino = USBclient()
        stringit = str(data)
        dataToSend = stringit.strip('')
        #Arduino .ino needs \n to read string
        #derp = derp.strip('\n')
        # Im leaving all the newlines foe debug reasons
        print ">"+dataToSend+"<"

        if dataToSend == 'Direction:\n':
            myArduino.cmdReceived("2\n")
        elif derp == 'Direction : Right\n':
            myArduino.cmdReceived("1\n")
        elif derp == 'Direction : Left\n':
            myArduino.cmdReceived("2\n")
        elif derp == 'Direction : Center\n':
            myArduino.cmdReceived("0\n")
        else:
            myArduino.cmdReceived("else\n")
            pass



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
SerialPort(USBclient(), '/dev/cu.wchusbserial410', reactor, baudrate='9600')
print 'server started on', Port
reactor.run()
