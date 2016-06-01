from twisted.internet import reactor
from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import time
import threading

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
        
        global timer
        timer = 0
        self.send(self.transport)
            
    def send(self, transport):
        message = bytearray()
      
        message.append('L')
        message.append('S')
        message.extend('2f8d2b5035e7e10d')
        message.append(0x0d)
        message.append(0x0a)
        message.append(0x04)

        transport.write(message) # no need for address
        
        message = bytearray()
      
        message.append('L')
        message.append('I')
        message.extend('2f8d2b5035e7e10d')
        message.append(0x0d)
        message.append(0x0a)
        message.append(0x04)

        transport.write(message) # no need for address

        count = 0
        while True:
            message = bytearray()
            
            if count < 10:
                
                message.append('L')
                message.append('F')
                message.extend('2f8d2b5035e7e10d')
                message.append(0x0d)
                message.append(0x0a)
                message.append(0x04)
                
            elif count < 20:
                message.append('L')
                message.append('I')
                message.extend('2f8d2b5035e7e10d')
                message.append(0x0d)
                message.append(0x0a)
                message.append(0x04)
                
            elif count < 30:
            
                message.append('L')
                message.append('B')
                message.extend('2f8d2b5035e7e10d')
                message.append(0x0d)
                message.append(0x0a)
                message.append(0x04)
                
            elif count < 40:
                message.append('L')
                message.append('I')
                message.extend('2f8d2b5035e7e10d')
                message.append(0x0d)
                message.append(0x0a)
                message.append(0x04)
                
            else:
                count = 0
                continue
            
            count += 1
           
            transport.write(message) # no need for address
                
            time.sleep(1)
    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)
        
        message = ''
        if self.count == 0:
            for byte in data:
                message += repr(byte)
                
        print message
        global timer
        
        timer = 0
        
    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"

# 0 means any port, we don't care in this case
reactor.listenUDP(0, Greeter())
reactor.run()
