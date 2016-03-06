from twisted.internet import reactor
from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet.endpoints import TCP4ClientEndpoint



class Greeter(DatagramProtocol):

    def startProtocol(self):
        host = "192.168.1.186"
        port = 9998

        self.count = 0
        self.b = bytearray()
        self.length = ''
        self.packets = 0

        self.transport.connect(host, port)
        print "now we can only send to host %s port %d" % (host, port)
        self.transport.write("hello") # no need for address

    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)

        if self.count == 0:

            for i in range(1, len(data)):
                self.length += data[i]
            self.packets = int(self.length)

            print self.packets
            self.count += 1

        else:
            self.b += data

            if self.count == self.packets:

                with open('test.jpg', 'wb') as output:
                    output.write(self.b)

                self.count = 0
                self.b = bytearray()
                self.length = ''
                self.packets = 0

            else:

                self.count += 1





    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"

# 0 means any port, we don't care in this case
reactor.listenUDP(0, Greeter())
reactor.run()
