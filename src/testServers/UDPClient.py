from twisted.internet import reactor
from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet.endpoints import TCP4ClientEndpoint



class Greeter(DatagramProtocol):

    def startProtocol(self):
        host = "127.0.0.1"
        port = 9998

        self.count = 0
        self.b = bytearray()
        self.length = ''
        self.packets = 0

        self.transport.connect(host, port)
        print "now we can only send to host %s port %d" % (host, port)
        message = bytearray()

        
        message.append('L')
        message.append('S')
        message.extend('2f8d2b5035e7e10d')
        message.append(0x0d)
        message.append(0x0a)
        message.append(0x04)

        self.transport.write(message) # no need for address

    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)
        
        message = ''
        if self.count == 0:
            for byte in data:
                message += repr(byte)
                
        print message
        
        return
        if True:
            self.count += 1

            self.packets = ord(data[6])

            
            #print self.packets
        else:
            #print ord(data[5])
            self.b += data[6:]

            if not self.count < self.packets:
                with open('test.jpg', 'wb') as output:
                    output.write(self.b)
                print len(self.b)
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
