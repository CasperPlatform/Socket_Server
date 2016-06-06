import serial
import time

def sendCmd(cmd):
    sPort = '/dev/cu.usbmodem411'
    ser = serial.Serial(sPort, 115200)
    for byte in cmd:
        ser.write(byte)

message = bytearray()
message.append(0x43)
message.append(0x49)
message.append(0x0)
message.append(0x49)
message.append(0x0)
message.append(0xd)
message.append(0xa)

i = 0
while True:
    if i == 0:
        message[1] = ord('L')
        message[2] = 90
    elif i == 1:
        message[1] = ord('R')
        message[2] = 90
    elif i == 2:
        message[3] = ord('U')
        message[4] = 90
    elif i == 3:
        message[3] = ord('D')
        message[4] = 50
        i = 0

    sendCmd(message)
    time.sleep(3)

    message[1] = ord('I')
    message[2] = 0
    message[3] = ord('I')
    message[4] = 0
