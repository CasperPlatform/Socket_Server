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
                tmp = ''
                datarec = bytearray()
                for byte in data:

                    # have to convert negative flagged values to negative values
                    # before sending via serial
                    datarec.append(ord(byte))
                    if hex(ord(byte)) == '0xd':
                        tmp = byte
                        continue
                    if hex(ord(byte)) == '0xa' and hex(ord(tmp)) == '0xd':
                        print 'got CLRF'
                        break
                print datarec


            # in case the data dosent match send "else"
            # this will be returned from arduino
            myArduino.cmdReceived(datarec)
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
