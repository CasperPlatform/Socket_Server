import sys
import twisted
from urlparse import urlparse
from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.serialport import SerialPort

serServ = None

class USBclient(Protocol):
    def connectionMade(self):
        global serServ
        serServ = self
        print 'Arduino device: ', serServ, ' is connected.'

    def cmdReceived(self, cmd):
        serServ.transport.write(cmd)
        print cmd, ' - sent to Arduino.'
        pass

    def dataReceived(self,data):
        print 'USBclient.dataReceived called with:'
        print str(data)

class HTTPserver(resource.Resource):
    isLeaf = True
    def render_GET(self, request):      #passes the data from the get request
        print 'HTTP request received'
        myArduino = USBclient()
        stringit = str(request)
        parse = stringit.split()
        command, path, version = parse
        myArduino.cmdReceived(path)

class cmdTransport(Protocol):
    def __init__(self, factory):
        self.factory = factory

class cmdTransportFactory(Factory):
    protocol = cmdTransport

if __name__ == '__main__':
    HTTPsetup = server.Site(HTTPserver())
    reactor.listenTCP(5002, HTTPsetup)
    SerialPort(USBclient(), '/dev/cu.wchusbserial410', reactor, baudrate='9600')
    reactor.run()
