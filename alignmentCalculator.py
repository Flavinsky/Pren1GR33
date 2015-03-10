__author__ = 'Dominic Schuermann'

import sys
import math

# define real environment fields - all dimensions in cm
realFieldSizeX = 150
realFieldSizeY = 250
binRadius = 30
startToBinCentroid = 225

# define camera environment fields - dimensions in px
cameraFieldSizeX = 1820


def calculateAngle(xToAdjust):

    print("Calculator - calculateAngle started")

    print ("xToAdjust", float(xToAdjust))
    print ("realFieldSizeX", realFieldSizeX)
    print ("cameraFieldSizeX", cameraFieldSizeX)
    realXtoAdjust = float(realFieldSizeX) / float(cameraFieldSizeX) * float(xToAdjust)
    print ("realXToAdjust", realXtoAdjust)

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

