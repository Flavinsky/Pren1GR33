__author__ = 'Dominic Schuermann'

import alignmentCalculator
import objectDetectionDom
import serial

rpmBLCD = 8000

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

    distanceToBin = objectDetectionDom.getDistanceToBin()

    calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)
    stepperCommand = alignmentCalculator.getCommand(calculatedAngle)

    out = ''
    serialConnection = openSerialConnection()

    print("----------------------------------------------------------------------")
    print("Agent - start BLDC")
    # startup BLDC
    serialConnection.write(b'BLDC on\r')
    sleep(0.5)

    serialConnection.write(b'BLDC setrpm' + rpmBLCD + '\r')
    sleep(0.5)

    while serialConnection.inWaiting() > 0:
        out + serialConnection.read(1)
        if out != '':
            print ">>" + out

    print("----------------------------------------------------------------------")
    print("Agent - align for shooting")
    # align robot to bin
    serialConnection.write(stepperCommand)

    while serialConnection.inWaiting() > 0:
        out + serialConnection.read(1)
        if out != '':
            print ">>" + out
        if out == 'job done':
            break

    print("----------------------------------------------------------------------")
    print("Agent - shoot!")
    # shoot!
    serialConnection.write(b'DC up\r')
    sleep(0.5)
    serialConnection.write(b'DC on')
    sleep(0.5)

    # sleep while shooting
    sleep(15)
    print("----------------------------------------------------------------------")
    print("Agent - job done!")
    print("======================================================================")
