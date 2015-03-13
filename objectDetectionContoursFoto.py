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

# define variable
threshold_value = config.getfloat('BinaryThreshold', 'threshold_value')
threshold_maxvalue = config.getfloat('BinaryThreshold', 'threshold_maxvalue')

# Bin width = 500px -> declare as max
# Bin width on left or right side is +/- 300px
# height defined with crop height of picture
binFullWidth = config.getfloat('Bin', 'binFullWidth')
binFullHeight = config.getfloat('Bin', 'binFullHeight')
binMinWidth = config.getfloat('Bin', 'binMinWidth')
binMinHeight = config.getfloat('Bin', 'binMinHeight')

binContourAreaMin = binMinWidth * binFullHeight
binContourAreaMax = binFullWidth * binFullHeight

binFullSizeMin = binFullWidth * binMinHeight
binFullSizeMax = binFullWidth * binFullHeight

# Centroids
pictureCentroidX = 0
pictureCentroidY = 0
contourCentroidX = 0
contourCentroidY = 0
differenceCentroidX = 0


# define on change method
def on_change(position):
    pass


def calculateCentroidX(cnt):
    cntMoments = cv2.moments(cnt)
    calculatedCentroidX = int(cntMoments['m10']/cntMoments['m00'])
    return calculatedCentroidX

#define trackbar
#cv2.createTrackbar('Threshold Value', 'window', threshold_value, threshold_maxvalue, on_change)



def getDistanceToBin():
#if __name__ == '__main__':

    print("----------------------------------------------------------------------")
    print("imageDetection - getDistanceToBin started")

    # capture video from camera

    # Take each frame
    #while True:

    image = cv2.imread('left.jpg')
    processingImage = image[1200:1450, 350:2242]
    referenceImage = processingImage.copy()

    # convert to greyscale
    processingGrey = cv2.cvtColor(processingImage, cv2.COLOR_BGR2GRAY)
    referenceGrey = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)

    # invert picture
    processingGreyInv = cv2.bitwise_not(processingGrey)
    processingGreyInvCopy = processingGreyInv.copy()
    referenceGreyInv = cv2.bitwise_not(referenceGrey)

    # create binary picture
    ret, binaryImage1 = cv2.threshold(processingGreyInvCopy, threshold_value, threshold_maxvalue, cv2.THRESH_BINARY)
    ret, binaryImage2 = cv2.threshold(processingGreyInvCopy, threshold_value, threshold_maxvalue, cv2.THRESH_BINARY)
    ret, binaryImage3 = cv2.threshold(processingGreyInvCopy, threshold_value, threshold_maxvalue, cv2.THRESH_BINARY)

    ret, referenceBinary = cv2.threshold(referenceGreyInv, 0, 255, cv2.THRESH_BINARY)

    # filtering
    kernel = np.ones((8, 8), np.uint8)
    filteredBinaryImage = cv2.morphologyEx(binaryImage3, cv2.MORPH_OPEN, kernel)
    filteredBinaryImage2 = filteredBinaryImage.copy()

    # evaluate full picture centroid
    referenceContours, fullHierarchy = cv2.findContours(referenceBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in referenceContours:

        # get centroid of whole picture, base reference for angle correction
        fullMoments = cv2.moments(cnt)
        fullCentroidX = int(fullMoments['m10']/fullMoments['m00'])
        fullCentroidY = int(fullMoments['m01']/fullMoments['m00'])
        cv2.circle(referenceImage, (fullCentroidX, fullCentroidY), 3, (0, 0, 255))
        #print(fullCentroidX)
        pictureCentroidX = fullCentroidX
        pictureCentroidY = fullCentroidY

    # evaluate contours on picture -> find bin
    contours2, hierarchy2 = cv2.findContours(filteredBinaryImage2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours2:
        contourArea = cv2.contourArea(cnt)
        if binContourAreaMin < contourArea < binContourAreaMax:

            cv2.drawContours(processingImage, [cnt], 0, (0, 255, 0), 2)

            # find and draw endpoints of contour
            hull = cv2.convexHull(cnt)
            for points in hull:
                point = points[0]
                cv2.circle(processingImage, (point[0], point[1]), 5, (0, 0, 255))

            # check if bin is fully seen in picture. if not, do special centroid calculation with reference size
            if not binFullSizeMin < contourArea < binFullSizeMax:
                #bin is not fully seen in picture
                print("----> non normal shape <----")
                # create reference bin shape for centroid calculation
                # referenceBinShape = np.array([(0, 0), (binFullSizeX, 0), (binFullSizeX, binFullSizeY), (0, binFullSizeY), (0, 0)], np.float32)

                referenceRelativeCentroidX = binFullWidth / 2
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


#         cv2.imshow('crop', processingImage)
#         cv2.imshow('contours (opening2)', filteredBinaryImage2)
#         cv2.imshow('binary (binaryImage2)', binaryImage2)
#         cv2.imshow('after filter (opening)', filteredBinaryImage)
#         cv2.imshow('fullBinary', referenceImage)
#         #
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# cv2.destroyAllWindows()

if __name__ == '__main__':
    print("----------------------------------------------------------------------")
    print("image detection started")
    sys.exit(getDistanceToBin())