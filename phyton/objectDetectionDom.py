__author__ = 'Dominic Schuermann'

# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import cv2
import numpy as np
import sys
import ConfigParser
import argparse

# define config parser
config = ConfigParser.RawConfigParser()
config.read('objectDetectionDefinition.cfg')

# define argsparser
argsparser = argparse.ArgumentParser(description='object detection logic')
argsparser.add_argument('-n', '--normal', dest='debugmode', action='store_false',
                        help='logic will be executed in normal mode')
argsparser.add_argument('-d', '--debug', dest='debugmode', action='store_true',
                        help='logic will be executed in debug mode')
argsparser.set_defaults(debugmode=False)
args = argsparser.parse_args()

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

def getDistanceToBin(debugmode):

    print("----------------------------------------------------------------------")
    print("imageDetection - getDistanceToBin started")

    # # initialize the camera and grab a reference to the raw camera capture
    # camera = PiCamera()
    # camera.resolution = (2592, 1944)
    # rawCapture = PiRGBArray(camera, size=(2592, 1944))
    #
    # # allow the camera to warmup
    # time.sleep(0.1)
    #
    # # grab an image from the camera
    # camera.capture(rawCapture, format="bgr")
    # img = rawCapture.array

    img = cv2.imread('images/newRight.jpg')

    # Read parameters
    height, width, depth = img.shape

    # calculate analyzed area
    borderX = paddingSideFactor * width
    borderY = paddingTopFactor * height
    analyzedWidth = width - 2 * borderX
    analyzedHeight = height * analysedAreaHeightFactor
    binMinArea = analyzedHeight * ReferenceBinWidth * areaThreshFactor

    contourMinArea = analyzedHeight * ReferenceBinWidth * contourMinThreshFactor
    contourMaxArea = analyzedHeight * ReferenceBinWidth

    processingImage = img[borderY:borderY + analyzedHeight, borderX:borderX + analyzedWidth]
    if(debugmode):
        cv2.imwrite("processing.jpg", processingImage)

    referenceImage = processingImage.copy()
    processImgDebug = processingImage.copy()

    # convert to greyscale
    processingGrey = cv2.cvtColor(processingImage, cv2.COLOR_BGR2GRAY)
    referenceGrey = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)

    # invert picture
    processingGreyInv = cv2.bitwise_not(processingGrey)
    processingGreyInvCopy = processingGreyInv.copy()
    referenceGreyInv = cv2.bitwise_not(referenceGrey)

    # create binary picture
    ret, binaryImage = cv2.threshold(processingGreyInvCopy, binaryThreshValue, binaryThreshMax, cv2.THRESH_BINARY)
    if(debugmode):
        cv2.imwrite("binary.jpg", binaryImage)

    ret, referenceBinary = cv2.threshold(referenceGreyInv, 0, 255, cv2.THRESH_BINARY)

    # filtering
    kernel = np.ones((8, 8), np.uint8)
    filteredBinaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_OPEN, kernel)
    filteredBinaryImage2 = filteredBinaryImage.copy()

    # evaluate full picture centroid
    referenceContours, fullHierarchy = cv2.findContours(referenceBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #init useable variables
    pictureCentroidX = 0
    pictureCentroidY = 0
    contourCentroidX = 0
    contourCentroidY = 0
    differenceCentroidX = 0

    for cnt in referenceContours:

        # get centroid of whole picture, base reference for angle correction
        fullMoments = cv2.moments(cnt)
        pictureCentroidX = int(fullMoments['m10']/fullMoments['m00'])
        pictureCentroidY = int(fullMoments['m01']/fullMoments['m00'])

    # evaluate contours on picture -> find bin
    contours2, hierarchy2 = cv2.findContours(filteredBinaryImage2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours2:
        contourArea = cv2.contourArea(cnt)
        
        if contourMinArea < contourArea < contourMaxArea:

            #draw contour for debug
            cv2.drawContours(processImgDebug,cnt,-1,(0,255,0),3)

            # find and draw endpoints of contour for debug
            hull = cv2.convexHull(cnt)
            for points in hull:
                point = points[0]
                cv2.circle(processImgDebug, (point[0], point[1]), 5, (0, 0, 255))

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

                # for debugging
                contourCentroidY = int(contourMoments['m01']/contourMoments['m00'])

                contourCentroidX = centroidX
                differenceCentroidX = 0

    #calculate difference to picture centroid
    if not (pictureCentroidX is 0):
        if not (contourCentroidX is 0):
            distanceToCentroid = pictureCentroidX - contourCentroidX

            # draw line for debugging
            print("px middle to cont raw", distanceToCentroid)

            if not (differenceCentroidX is None):
                # centroid correction if needed
                if distanceToCentroid < 0:
                    distanceToCentroid -= differenceCentroidX

                    if(debugmode):
                        cv2.line(processImgDebug, (pictureCentroidX, pictureCentroidY), (int(contourCentroidX + differenceCentroidX), contourCentroidY), (0, 255, 0), 2)
                        cv2.line(processImgDebug, (pictureCentroidX, pictureCentroidY), (contourCentroidX, contourCentroidY),(255, 0, 0), 5)

                elif distanceToCentroid >= 0:
                    distanceToCentroid += differenceCentroidX

                    if(debugmode):
                        cv2.line(processImgDebug, (pictureCentroidX, pictureCentroidY), (int(contourCentroidX - differenceCentroidX), contourCentroidY), (0, 255, 0), 2)
                        cv2.line(processImgDebug, (pictureCentroidX, pictureCentroidY), (contourCentroidX, contourCentroidY),(255, 0, 0), 5)

            print("px middle to cont corrected", distanceToCentroid)

            cv2.imwrite("contours.jpg", processImgDebug)

            return distanceToCentroid
        else:
            print("contourCentroidX not defined - No processable contour found!")
            return 0
    else:
        print("pictureCentroidX not defined - No processable picture found!")
        return 0

if __name__ == '__main__':
    print("----------------------------------------------------------------------")
    if(args.debugmode):
        print("image detection started - DEBUG")
    else:
        print("image detection started")
    sys.exit(getDistanceToBin(args.debug))