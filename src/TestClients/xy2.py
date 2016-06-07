import serial
import time

sPort = '/dev/cu.usbmodem411'
ser = serial.Serial(sPort, 9600)

def sendCmd():
    ser.write(b"C")
    ser.write(b"R")
    ser.write(b"180")
    ser.write(b"U")
    ser.write(b"180")
    ser.write(b"\n")



def sendCmd2():
    ser.write(b"C")
    ser.write(b"R")
    ser.write(b"90")
    ser.write(b"U")
    ser.write(b"90")
    ser.write(b"\n")


sendCmd()
time.sleep(3)
sendCmd2()
