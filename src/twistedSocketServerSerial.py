from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
import sys
import serial

from enum import Enum

class typeFlag(Enum):
    Drive = 'D'
class directionFlag(Enum):
    Forward  = 'F'
    Backward = 'B'
    Idle     = 'I'
class angleFlag(Enum):
    Right = 'R'
    Left  = 'L'
    Idle  = 'I'

serServ = None

class USBclient(Protocol):
    def connectionMade(self):
        global serServ
        serServ = self
        #serServ.transport.write()
        print 'Arduino device: ', serServ, ' is connected.'

    def cmdReceived(self, cmd):
        #serServ.transport.write(cmd)
        for byte in cmd:
            serServ.transport.write(chr(byte))
        #leaving all newlines for debug reasons
        #print cmd, ' - sent to Arduino.'

    def dataReceived(self,data):
        print 'USBclient.dataReceived called with:'
        print data

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
        # stringit = str(data)
        # dataToSend = stringit.strip('')
        # #Arduino .ino needs \n to read string
        # #derp = derp.strip('\n')
        # # Im leaving all the newlines foe debug reasons
        # print ">"+dataToSend+"<"
        #
        # # convert the data sent from Client to numbers
        # # relateing to motor control on the Arduino
        # if dataToSend == 'Direction:\n':
        #     myArduino.cmdReceived("2\n")
        # elif derp == 'Direction : Right\n':
        #     myArduino.cmdReceived("1\n")
        # elif derp == 'Direction : Left\n':
        #     myArduino.cmdReceived("2\n")
        # elif derp == 'Direction : Center\n':
        #     myArduino.cmdReceived("0\n")
        # else:
        #     # in case the data dosent match send "else"
        #     # this will be returned from arduino
        #     myArduino.cmdReceived("else\n")
        #     pass

        tmp = ''
        tf   = typeFlag.Drive
        df   = directionFlag.Forward
        af   = angleFlag.Right
        speed = 0
        angle = 0

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
        if datarec[0] != ord(typeFlag.Drive):
             print repr(datarec[0])
             print 'unknown typeFlag...aborting'
             return
        else:
            tf = typeFlag.Drive
            print 'this is a driveMsg'

        if datarec[1] == ord(directionFlag.Forward) or datarec[1] == ord(directionFlag.Backward) or datarec[1] == ord(directionFlag.Idle):
            if datarec[1] == ord(directionFlag.Forward):
                print 'direction: Forward'
                df = directionFlag.Forward
            if datarec[1] == ord(directionFlag.Backward):
                print 'direction: Back'
                df = directionFlag.Backward
            if datarec[1] == ord(directionFlag.Idle):
                print 'direction: Idle'
                df = directionFlag.Idle
        else:
            print 'unknown DirectionFlag..aborting'
            return
        if datarec[2] == ord(angleFlag.Right) or datarec[2] == ord(angleFlag.Left) or datarec[2] == ord(angleFlag.Idle):
            if datarec[2] == ord(angleFlag.Right):
                print 'angle: Right'
                df = angleFlag.Right
            if datarec[2] == ord(angleFlag.Left):
                print 'angle: Left'
                df = angleFlag.Left
            if datarec[2] == ord(angleFlag.Idle):
                print 'angle: Idle'
                df = angleFlag.Idle
        else:
            print 'unknown AngleFlag..aborting'
            for i,byte in enumerate(datarec):
                print repr(byte),' '
            return
        if datarec[3] < 0 or datarec[3] > 255:
            print 'invalid Speed Value, aborting...'
            return
        else:
            speed = datarec[3]
            print 'speed : ',speed
        if datarec[4] < 0 or datarec[4] > 90:
            print 'invalid Angle Value, aborting...'
            return
        else:
            angle = datarec[4]
            print 'angle : ',angle

        print 'successfully parsed buffer!, sending to serial'
        myArduino.cmdReceived(datarec)
        #
        # for i,byte in enumerate(datarec):
        #     print repr(byte),' '




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
SerialPort(USBclient(), '/dev/ttyACM0', reactor, baudrate='9600')
print 'server started on', Port
reactor.run()
