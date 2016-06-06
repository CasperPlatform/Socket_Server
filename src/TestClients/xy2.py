import serial
import time

def sendCmd():
    sPort = '/dev/cu.usbmodem411'
    ser = serial.Serial(sPort, 115200)
    ser.write("180\n")


def sendCmd2():
    sPort = '/dev/cu.usbmodem411'
    ser = serial.Serial(sPort, 115200)
    ser.write("90\n")




sendCmd()
time.sleep(3)
sendCmd2()
