__author__ = 'Dominic Schuermann'

import sys
import math
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('alignmentCalculatorDefinitions.cfg')

# define real environment fields - all dimensions in cm
realFieldSizeX = config.getfloat('RealField', 'realFieldSizeX')
realFieldSizeY = config.getfloat('RealField', 'realFieldSizeY')
binRadius = config.getfloat('RealField', 'binRadius')
startToBinCentroidY = config.getfloat('RealField', 'startToBinCentroidY')

# define camera environment fields - dimensions in px
cameraFieldSizeX = config.getfloat('CameraField', 'cameraFieldSizeX')


def calculateAngle(xToAdjust):

    print("----------------------------------------------------------------------")
    print("Calculator - calculateAngle started")

    print ("xToAdjust", float(xToAdjust))
    print ("realFieldSizeX", realFieldSizeX)
    print ("cameraFieldSizeX", cameraFieldSizeX)
    realXtoAdjust = float(realFieldSizeX) / float(cameraFieldSizeX) * float(xToAdjust)
    print ("realXToAdjust", realXtoAdjust)

    # calculate angle to correct
    angleInRadians = math.atan(float(realXtoAdjust) / float(startToBinCentroidY))
    print ("angle in radians", angleInRadians)
    angleInDegrees = math.degrees(angleInRadians)
    print ("angle in degrees", angleInDegrees)

    return angleInDegrees

if __name__ == '__main__':
    print("calculator started")
    distanceToBin = sys.argv[1]
    sys.exit(calculateAngle(distanceToBin))

