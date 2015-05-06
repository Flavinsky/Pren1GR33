import cv2
import numpy as np
import ConfigParser

def detectBin():

    # define config parser
    config = ConfigParser.RawConfigParser()
    config.read('objectDetectionDefinition.cfg')

    # Parameters
    # FIXED_WIDTH = 1000
    ANALYZED_PART = config.getfloat('Image', 'AnalysedAreaHeightFactor')
    BORDER_PART = paddingSideFactor = config.getfloat('Image', 'PaddingSideFactor')
    TOP_PADDING = config.getfloat('Image', 'PaddingTopFactor')
    WINDOW_NAME = 'Test von Raffi'
    IMAGE_NAME = 'right.jpg'
    BIN_WIDTH = config.getfloat('Bin', 'ReferenceBinWidth')
    THRESHOLD_AREA = config.getfloat('Threshold', 'AreaThreshFactor')
    THRESHOLD_HEIGHT = config.getfloat('Threshold', 'AreaThreshFactor')

    # Create Window
    # cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    # Read image and parameters
    img = cv2.imread(IMAGE_NAME)
    height, width, depth = img.shape
    print(width)

    # calculate analyzed area
    borderX = BORDER_PART * width
    borderY = TOP_PADDING * height
    analyzedWidth = width - 2 * borderX
    analyzedHeight = height * ANALYZED_PART
    binMinArea = analyzedHeight * BIN_WIDTH * THRESHOLD_AREA
    middle = analyzedWidth / 2

    img2Analyze = img[borderY:borderY + analyzedHeight, borderX:borderX + analyzedWidth]
    img2Print = img[0:height, 0:width]

    binaryThreshValue = config.getfloat('Threshold', 'BinaryThreshValue')
    binaryThreshMax = config.getfloat('Threshold', 'BinaryThreshMax')

    lower = [255-binaryThreshMax, 255-binaryThreshMax, 255-binaryThreshMax]
    upper = [255-binaryThreshValue, 255-binaryThreshValue, 255-binaryThreshValue]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(img2Analyze, lower, upper)
    output = cv2.bitwise_and(img2Analyze, img2Analyze, mask=mask)

    imgray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    thresh = 20
    im_bw = cv2.threshold(imgray, thresh, 255, cv2.THRESH_BINARY)[1]
    ret, thresh = cv2.threshold(im_bw, 127, 255, 0)

    print("---- Detect contours ----")
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("- " + str(len(contours)) + " contours detected.")
    # cv2.line(img2Print, (int(middle + borderX), 0), (int(middle + borderX), int(height)), (0, 255, 0), thickness=5)

    for cont in contours:
        # get properties of contour
        x1, y1, w, h = cv2.boundingRect(cont)
        area = w * h
        print("- Width of detected contour: " + str(w))
        print("- Height of detected contour: " + str(h))
        print("- Area of detected contour: " + str(area))

        # check if contour is high enough to be the bin
        if h > analyzedHeight * THRESHOLD_HEIGHT:

            print("- " + str(h) + " > " + str(analyzedHeight) + " * " + str(THRESHOLD_HEIGHT) + " = " + str(analyzedHeight * THRESHOLD_HEIGHT))

            # find center of contour
            (x, y), radius = cv2.minEnclosingCircle(cont)
            print("- Center of contour: (X:"+str(x)+", Y:"+str(y))
            # print line from middle of board to center of detected object
            #cv2.line(img2Print, (int(middle + borderX), int(borderY +y)), (int(x + borderX), int(borderY +y)), (0, 0, 255), thickness=10)
            # The gap is the distance between the detected center of the bin and the effective center
            # (some parts may be outside the analyzed area)
            gap = 0

            # check if the hole bin is on the analyzed part of the image
            if area < binMinArea:
                gap = BIN_WIDTH / 2 - w / 2
                gap = -gap if x < middle else gap

            print("- Border correction: "+str(gap))

            # print line from middle of board to effectife center of object
            # cv2.line(img2Print, (int(middle + borderX), int(borderY + y)), (int(x + gap + borderX),  int(borderY + y)), (0, 255, 255), thickness=5)
            lineLength = x + gap - middle
            break

    print ("- Distance to center of board: "+ str(lineLength))
    return lineLength

    # show the images
    # cv2.imshow(WINDOW_NAME, img2Print)


    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    detectBin()