__author__ = 'Dominic Schuermann'


print("Starting connection test to freescale freedomboard")

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


ser.write(b'BLDC on\r\n')
sleep(0.5)

ser.write(b'BLDC setrpm 2000\r\n')
sleep(0.5)

ser.write(b'BLDC status\r\n')
sleep(0.5)

ser.write(b'BLDC setrpm 0\r\n')
sleep(0.5)

ser.write(b'BLDC off\r\n')
sleep(0.5)

while ser.inWaiting() > 0:
    out += ser.read(1)

if out != '':
    print ">>" + out

ser.close()