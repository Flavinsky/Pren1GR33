__author__ = 'Dominic Schuermann'

import alignmentCalculator
import objectDetectionDom


if __name__ == '__main__':
    print("agent started")

    distanceToBin = objectDetectionDom.getDistanceToBin()

    calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)
    print (calculatedAngle)
