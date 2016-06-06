import serial
import time

def sendCmd(cmd):
    sPort = '/dev/ttyACM0'
    ser = serial.Serial(sPort, 9600)

    for byte in cmd:
        ser.write(chr(byte))

message = bytearray()
message.append(hex('C'))
message.extend(hex('I'))
message.extend(0x0)
message.extend(hex('I'))
message.extend(0x0)
message.extend(0xd)
message.extend(0xa)

i = 0
while True:
    if i == 0:
        message[1] = hex('L')
        message[2] = hex(90)
    elif i == 1:
        message[1] = hex('R')
        message[2] = hex(90)
    elif i == 2:
        message[3] = hex('U')
        message[4] = hex(90)
    elif i == 3:
        message[3] = hex('D')
        message[4] = hex(50)
        i = 0

    sendCmd(message)
    time.sleep(3)

    message[1] = hex('I')
    message[2] = hex(0)
    message[3] = hex('I')
    message[4] = hex(0)
