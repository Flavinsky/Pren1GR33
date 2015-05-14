__author__ = 'orceN'

import serial
import sys
from time import sleep

def openSerialConnection():
    print("----------------------------------------------------------------------")
    print("Initialisation - initialize serial connection")

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
    print("Initialisation started")

    out = ''
    serialConnection = openSerialConnection()

    print("----------------------------------------------------------------------")
    print ("initialize Stepper")

    serialConnection.write(b'stepper reset\r')
    sleep(0.5)
    serialConnection.write(b'stepper initposition r 30000\r')
    sleep(3)
    serialConnection.write(b'stepper home set\r')
    sleep(0.5)

    print("----------------------------------------------------------------------")
    print ("initialize BLDC")

    serialConnection.write(b'BLDC init\r')
    sleep(2)

    while serialConnection.inWaiting() > 0:
        out + serialConnection.read(1)
    if out != '':
        print ">>" + out

    print("----------------------------------------------------------------------")
    print("Initialisation done")
    print("======================================================================")