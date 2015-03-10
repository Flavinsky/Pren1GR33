__author__ = 'Dominic Schuermann'

import sys
import math

# define real environment fields - all dimensions in cm
fieldSizeX = 150
fieldSizeY = 250
binRadius = 30
startToBinCentroid = 225

# define camera environment fields - dimensions in px
realFieldSizeX = 1820


def calculateAngle(xToAdjust):

    print("Calculator - createAngle started")

    print ("xToAdjust", float(xToAdjust))
    print ("fieldSizeX", fieldSizeX)
    print ("realFieldSizeX", realFieldSizeX)
    realXtoAdjust = float(fieldSizeX) / float(realFieldSizeX) * float(xToAdjust)
    print ("realToAdjust", realXtoAdjust)

    # calculate angle to correct
    angleInRadians = math.atan(float(realXtoAdjust) / float(startToBinCentroid))
    print ("angle in radians", angleInRadians)
    angleInDegrees = math.degrees(angleInRadians)
    print ("angle in degrees", angleInDegrees)

    return angleInDegrees

if __name__ == '__main__':
    print("calculator started")
    distanceToBin = sys.argv[1]
    sys.exit(calculateAngle(distanceToBin))

