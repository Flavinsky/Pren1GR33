__author__ = 'Dominic Schuermann'

import unittest
import alignmentCalculator


class alignmentCalculatorTests(unittest.TestCase):

    # test with -800
    def testCalculateAngleMinus800(self):

        distanceToBin = -800
        calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)

        self.failUnlessEqual(round(calculatedAngle, 2), -16.33)

    def testCalculatedAngleMinus5(self):

        distanceToBin = -5
        calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)

        self.failUnlessEqual(round(calculatedAngle, 2), -0.1)

    def testCalculatedAngleZero(self):

        distanceToBin = 0
        calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)

        self.failUnlessEqual(round(calculatedAngle, 2), 0)

    def testCalculatedAnglePlus150(self):

        distanceToBin = 150
        calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)

        self.failUnlessEqual(round(calculatedAngle, 2), 3.14)

    def testCalculatedAnglePlus650(self):

        distanceToBin = 650
        calculatedAngle = alignmentCalculator.calculateAngle(distanceToBin)

        self.failUnlessEqual(round(calculatedAngle, 2), 13.39)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

