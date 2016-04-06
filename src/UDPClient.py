from twisted.internet import reactor
from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet.endpoints import TCP4ClientEndpoint



class Greeter(DatagramProtocol):

    def startProtocol(self):
        host = "192.168.10.1"
        port = 6000

        self.count = 0
        self.b = bytearray()
        self.length = ''
        self.packets = 0

        self.transport.connect(host, port)
        print "now we can only send to host %s port %d" % (host, port)
        message = bytearray()

        message.append(0x01)
        message.extend('2dd1a34ccc12c65a')
        messaged.append('S')

        self.transport.write("hello") # no need for address

    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)

        if self.count == 0:
            #print data
            self.count += 1

            self.packets = ord(data[6])

            #print self.packets
        else:
            #print ord(data[5])
            self.b += data[6:]

            if not self.count < self.packets:
                with open('test.jpg', 'wb') as output:
                    output.write(self.b)

                self.count = 0
                self.b = bytearray()
                self.length = ''
                self.packets = 0

                print 'Image recieved'

            else:
                self.count += 1

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"

# 0 means any port, we don't care in this case
reactor.listenUDP(0, Greeter())
reactor.run()
