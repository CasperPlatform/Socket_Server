import serial
import time

def sendCmd():
    sPort = '/dev/cu.usbmodem411'
    ser = serial.Serial(sPort, 115200)
    cmd = bytearray()
    cmd = ''.join(chr(x) for x in [0x43,0x52,0x78,0x55,0x78])
    ser.write(cmd)


def sendCmd2():
    sPort = '/dev/cu.usbmodem411'
    ser = serial.Serial(sPort, 115200)
    cmd = ''.join(chr(x) for x in [0x43,0x49,0x00,0x49,0x00])
    ser.write(cmd)

cmd = bytearray()
sPort = '/dev/cu.usbmodem411'
ser = serial.Serial(sPort, 115200)
cmd = ''.join(chr(x) for x in [0x43,0x52,0x78,0x55,0x78,0x0d,0x0a])
ser.write(cmd)
print repr(cmd)

while(True):
    print ser.readline()
