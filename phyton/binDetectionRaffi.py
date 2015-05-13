#from picamera.array import PiRGBArray
#from picamera import PiCamera
import cv2
import time
import numpy as np
import ConfigParser


def detectBin():

    showOutput = False
    takePicture = False

    # define config parser
    config = ConfigParser.RawConfigParser()
    config.read('objectDetectionDefinition.cfg')

    # Parameters
    # FIXED_WIDTH = 1000
    ANALYZED_PART = config.getfloat('Image', 'AnalysedAreaHeightFactor')
    BORDER_PART = paddingSideFactor = config.getfloat('Image', 'PaddingSideFactor')
    TOP_PADDING = config.getfloat('Image', 'PaddingTopFactor')
    WINDOW_NAME = 'Test von Raffi'
    IMAGE_NAME = 'images/newMiddle.jpg'
    BIN_WIDTH = config.getfloat('Bin', 'ReferenceBinWidth')
    THRESHOLD_AREA = config.getfloat('Threshold', 'AreaThreshFactor')
    THRESHOLD_HEIGHT = config.getfloat('Threshold', 'AreaThreshFactor')

    # Create Window
    if showOutput:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    if takePicture:
        camera = PiCamera()
        camera.resolution = (2592, 1944)
        rawCapture = PiRGBArray(camera, size=(2592, 1944))
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        del(camera)
        IMAGE_NAME = "CaptureRaffi.jpg"
        cv2.imwrite(IMAGE_NAME, img)

    # Read image and parameters
    img = cv2.imread(IMAGE_NAME)
    height, width, depth = img.shape
    print(width)

    # calculate analyzed area
    borderX = BORDER_PART * width
    borderY = TOP_PADDING * height
    analyzedWidth = width - 2 * borderX
    analyzedHeight = height * ANALYZED_PART
    print("analyzedHeight: " + str(analyzedHeight) )
    binMinArea = analyzedHeight * BIN_WIDTH * THRESHOLD_AREA
    middle = analyzedWidth / 2

    img2Analyze = img[borderY:borderY + analyzedHeight, borderX:borderX + analyzedWidth]
    img2Print = img[0:height, 0:width]

    cv2.rectangle(img2Print, (int(borderX),int(borderY)),(int(borderX+analyzedWidth),int(borderY+analyzedHeight)),(0,0,255),3)

    binaryThreshValue = config.getfloat('Threshold', 'BinaryThreshValue')
    binaryThreshMax = config.getfloat('Threshold', 'BinaryThreshMax')

    print("---- Detect contours ----")

    # convert to greyscale
    imgGrey = cv2.cvtColor(img2Analyze, cv2.COLOR_BGR2GRAY)

    # invert picture
    imgGreyInverted = cv2.bitwise_not(imgGrey)

    # create binary picture
    ret, binaryImage = cv2.threshold(imgGreyInverted, 150, 255, cv2.THRESH_BINARY)
    if showOutput:
        cv2.imshow("Binary Image", binaryImage)

    # filtering
    kernel = np.ones((8, 8), np.uint8)
    filteredBinaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(filteredBinaryImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("- " + str(len(contours)) + " contours detected.")

    lineLength = 0

    for cont in contours:
        # get properties of contour
        x1, y1, w, h = cv2.boundingRect(cont)
        area = w * h
        print("- Width of detected contour: " + str(w))
        print("- Height of detected contour: " + str(h))
        print("- Area of detected contour: " + str(area))

        # check if contour is high enough to be the bin
        if h > analyzedHeight * THRESHOLD_HEIGHT:

            if showOutput:
                x2,y2,w2,h2 = cv2.boundingRect(cont)
                cv2.rectangle(img2Print,(int(x2+ borderX),int(y2+borderY)),(int(x2+w2+ borderX),int(y2+h2+borderY)),(0,255,0),2)

            print("- " + str(h) + " > " + str(analyzedHeight) + " * " + str(THRESHOLD_HEIGHT) + " = " + str(analyzedHeight * THRESHOLD_HEIGHT))

            # find center of contour
            (x, y), radius = cv2.minEnclosingCircle(cont)
            print("- Center of contour: (X:"+str(x)+", Y:"+str(y))
            # print line from middle of board to center of detected object
            if showOutput:
                cv2.line(img2Print, (int(middle + borderX), int(borderY +y)), (int(x + borderX), int(borderY +y)), (0, 0, 255), thickness=10)
            # The gap is the distance between the detected center of the bin and the effective center
            # (some parts may be outside the analyzed area)
            gap = 0

            print("BinMinArea: "+str(binMinArea))
            print("Area: "+str(area))
            # check if the hole bin is on the analyzed part of the image
            if area < binMinArea:
                gap = BIN_WIDTH / 2 - w / 2
                gap = -gap if x < middle else gap

            print("- Border correction: "+str(gap))

            # print line from middle of board to effectife center of object
            if showOutput:
                cv2.line(img2Print, (int(middle + borderX), int(borderY + y)), (int(x + gap + borderX),  int(borderY + y)), (0, 255, 255), thickness=5)
            lineLength = x + gap - middle
            break

    print ("- Distance to center of board: "+ str(lineLength))
    # return lineLength
    if showOutput:
        cv2.line(img2Print, (int(middle + borderX), 0), (int(middle + borderX), int(height)), (0, 255, 0), thickness=5)
        # show the images
        cv2.imshow(WINDOW_NAME, img2Print)


        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    detectBin()