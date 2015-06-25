__author__ = 'Dominic Schuermann'

import alignmentCalculator
import objectDetectionDom
import serial
import sys
from time import sleep

def openSerialConnection():
    print("----------------------------------------------------------------------")
    print("Agent - initialize serial connection")

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
    print("Agent - started")

    distanceToBin = objectDetectionDom.getDistanceToBin(False)
    command = alignmentCalculator.calculateAngle(distanceToBin)

    if not(distanceToBin):
        sys.exit()

    out = ''
    serialConnection = openSerialConnection()

    print("----------------------------------------------------------------------")
    print("Agent - align for shooting")

    print('steppercommand:' + command)

    stprCommand = str(command)

    serialConnection.write(stprCommand)
    sleep(0.5)
    serialConnection.write('\r')
    sleep(0.5)

    while serialConnection.inWaiting() > 0:
        out + serialConnection.read(1)
    if out != '':
        print ">>" + out

    print("----------------------------------------------------------------------")
    print("Agent - shoot!")
    # shoot!
    serialConnection.write(b'DC up\r')
    sleep(0.5)
    serialConnection.write(b'DC on\r')
    sleep(0.5)

    # sleep while shooting
    sleep(6)

    print("----------------------------------------------------------------------")
    print("Agent - job done!")
    print("======================================================================")