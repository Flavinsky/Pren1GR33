__author__ = 'orceN'

import serial
import sys
from time import sleep

def openSerialConnection():
    print("----------------------------------------------------------------------")
    print("Shut down - initialize serial connection")

    ser = serial.Serial('/dev/ttyACM0', 38400)

    # check the connection
    if ser.isOpen() == True:
        print("connection ok")
        return ser
    else:
        print("connection failed")
        print("exiting...")
        sys.exit()

if __name__ == '__main__':
    print("======================================================================")
    print("Shut down")

    out = ''
    serialConnection = openSerialConnection()

    serialConnection.write(b'DC off\r')
    sleep(0.5)
    serialConnection.write(b'BLDC off\r')
    sleep(0.5)
    serialConnection.write(b'stepper home go\r')
    sleep(0.5)
    serialConnection.write(b'BLDC init\r')
    sleep(4)
    serialConnection.write(b'stepper softhiz\r')
    sleep(0.5)

    print("shut down")
    print("======================================================================")

