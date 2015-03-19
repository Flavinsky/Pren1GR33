__author__ = 'Dominic Schuermann'


import cv2
import numpy as np
import sys
import ConfigParser

# define config parser
config = ConfigParser.RawConfigParser()
config.read('objectDetectionDefinition.cfg')

# define window
cv2.namedWindow('window')

# define threshold
binaryThreshValue = config.getfloat('Threshold', 'BinaryThreshValue')
binaryThreshMax = config.getfloat('Threshold', 'BinaryThreshMax')
contourMinThreshFactor = config.getfloat('Threshold', 'ContourMinThreshFactor')
contourMaxThreshFactor = config.getfloat('Threshold', 'ContourMaxThreshFactor')

# define processed image size
paddingTopFactor = config.getfloat('Image', 'PaddingTopFactor')
paddingSideFactor = config.getfloat('Image', 'PaddingSideFactor')
analysedAreaHeightFactor = config.getfloat('Image', 'AnalysedAreaHeightFactor')

# Contour Area Threshold
areaThreshFactor = config.getfloat('Threshold', 'AreaThreshFactor')

# Bin reference size in px
ReferenceBinWidth = config.getfloat('Bin', 'ReferenceBinWidth')

# Read image and parameters
img = cv2.imread('right.jpg')
height, width, depth = img.shape

# calculate analyzed area
borderX = paddingSideFactor * width
borderY = paddingTopFactor * height
analyzedWidth = width - 2 * borderX
analyzedHeight = height * analysedAreaHeightFactor
binMinArea = analyzedHeight * ReferenceBinWidth * areaThreshFactor

contourMinArea = analyzedHeight * ReferenceBinWidth * contourMinThreshFactor
contourMaxArea = analyzedHeight * ReferenceBinWidth

# Centroids
pictureCentroidX = 0
pictureCentroidY = 0
contourCentroidX = 0
contourCentroidY = 0
differenceCentroidX = 0


def getDistanceToBin():

    print("----------------------------------------------------------------------")
    print("imageDetection - getDistanceToBin started")


    processingImage = img[borderY:borderY + analyzedHeight, borderX:borderX + analyzedWidth]
    referenceImage = processingImage.copy()
    displayImage = processingImage.copy()

    # convert to greyscale
    processingGrey = cv2.cvtColor(processingImage, cv2.COLOR_BGR2GRAY)
    referenceGrey = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)

    # invert picture
    processingGreyInv = cv2.bitwise_not(processingGrey)
    processingGreyInvCopy = processingGreyInv.copy()
    referenceGreyInv = cv2.bitwise_not(referenceGrey)

    # create binary picture
    ret, binaryImage = cv2.threshold(processingGreyInvCopy, binaryThreshValue, binaryThreshMax, cv2.THRESH_BINARY)

    ret, referenceBinary = cv2.threshold(referenceGreyInv, 0, 255, cv2.THRESH_BINARY)

    # filtering
    kernel = np.ones((8, 8), np.uint8)
    filteredBinaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_OPEN, kernel)
    filteredBinaryImage2 = filteredBinaryImage.copy()

    # evaluate full picture centroid
    referenceContours, fullHierarchy = cv2.findContours(referenceBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in referenceContours:

        # get centroid of whole picture, base reference for angle correction
        fullMoments = cv2.moments(cnt)
        pictureCentroidX = int(fullMoments['m10']/fullMoments['m00'])
        pictureCentroidY = int(fullMoments['m01']/fullMoments['m00'])

    # evaluate contours on picture -> find bin
    contours2, hierarchy2 = cv2.findContours(filteredBinaryImage2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours2:
        contourArea = cv2.contourArea(cnt)

        print("contourArea", contourArea)
        print("contourMinArea", contourMinArea)
        print("contourMaxArea", contourMaxArea)
        if contourMinArea < contourArea < contourMaxArea:

            cv2.drawContours(displayImage, [cnt], 0, (0, 255, 0), 2)

            # find and draw endpoints of contour
            hull = cv2.convexHull(cnt)
            for points in hull:
                point = points[0]
                cv2.circle(processingImage, (point[0], point[1]), 5, (0, 0, 255))

            # check if bin is fully seen in picture. if not, do special centroid calculation with reference size
            if contourArea < binMinArea:
                #bin is not fully seen in picture
                print("----> non normal shape <----")

                referenceRelativeCentroidX = ReferenceBinWidth / 2
                print("refRelCentX", referenceRelativeCentroidX)

                x,y,w,h = cv2.boundingRect(cnt)
                contourRelativeCentroidX = w / 2
                print("contRelCentX", contourRelativeCentroidX)

                #calculate difference
                differenceCentroidX = referenceRelativeCentroidX - contourRelativeCentroidX
                print("diffCentroidX", differenceCentroidX)

                # calc contour centroid
                contourMoments = cv2.moments(cnt)
                contourCentroidX = int(contourMoments['m10']/contourMoments['m00'])
                # for debugging
                contourCentroidY = int(contourMoments['m01']/contourMoments['m00'])

                print("contAbsCentX", contourCentroidX)

            else:
                # bin is fully seen in picture
                # calculate centroid
                print("----> normal shape <----")
                contourMoments = cv2.moments(cnt)
                centroidX = int(contourMoments['m10']/contourMoments['m00'])
                centroidY = int(contourMoments['m01']/contourMoments['m00'])
                cv2.circle(processingImage, (centroidX, centroidY), 3, (0, 150, 0))
             #   print(centroidX)
                contourCentroidX = centroidX
                contourCentroidY = centroidY
                differenceCentroidX = 0

    #calculate difference to picture centroid
    if not (pictureCentroidX is None):
        if not (contourCentroidX is None):
            distanceToCentroid = pictureCentroidX - contourCentroidX

            # draw line for debugging
            print("px middle to cont raw", distanceToCentroid)
            cv2.line(referenceImage, (pictureCentroidX, pictureCentroidY), (contourCentroidX, contourCentroidY), (0, 0, 255), 6)

            if not (differenceCentroidX is None):
                # centroid correction if needed
                if distanceToCentroid < 0:
                    distanceToCentroid -= differenceCentroidX
                    # draw line for debugging
                    cv2.line(referenceImage, (pictureCentroidX, pictureCentroidY), (int(contourCentroidX + differenceCentroidX), contourCentroidY), (0, 255, 0), 2)

                elif distanceToCentroid >= 0:
                    distanceToCentroid += differenceCentroidX
                    # draw line for debugging
                    cv2.line(referenceImage, (pictureCentroidX, pictureCentroidY), (int(contourCentroidX - differenceCentroidX), contourCentroidY), (0, 255, 0), 2)

            print("px middle to cont corrected", distanceToCentroid)

            return distanceToCentroid

if __name__ == '__main__':
    print("----------------------------------------------------------------------")
    print("image detection started")
    sys.exit(getDistanceToBin())