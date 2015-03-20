__author__ = 'Dominic Schuermann'

print("Starting connection test for Stepper")

import sys
import serial
from time import sleep

# open the serial connection (check with dmesg if it's not working)
ser = serial.Serial('/dev/ttyACM0', 38400)

out = ''

# check the connection
if ser.isOpen() == True:
    print("connection ok")
else:
    print("connection failed")
    print("exiting...")
    sys.exit()