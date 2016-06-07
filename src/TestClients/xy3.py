import serial
import time


ser = serial.Serial('/dev/cu.usbmodem411', 115200)

ser.write(b"0")
ser.write(b'\n')
