__author__ = 'Dominic Schuermann'

import alignmentCalculator
import objectDetectionContoursFoto


if __name__ == '__main__':
    print("agent started")

    distanceToBin = objectDetectionContoursFoto.getDistanceToBin()

    calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)
    print (calculatedAngle)
