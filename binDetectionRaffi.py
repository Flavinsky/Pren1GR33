import cv2
import numpy as np

# Parameters
# FIXED_WIDTH = 1000
ANALYZED_PART = 0.1
BORDER_PART = 0.16
TOP_PADDING = 0.6
WINDOW_NAME = 'Test von Raffi'
IMAGE_NAME = 'right.jpg'
BIN_WIDTH = 453
THRESHOLD_AREA = 0.97
THRESHOLD_HEIGHT = 0.95

# Create Window
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

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

lower = [0, 0, 0]
upper = [70, 70, 70]

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

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.line(img2Print, (int(middle + borderX), 0), (int(middle + borderX), int(height)), (0, 255, 0), thickness=5)

for cont in contours:
    # get properties of contour
    x1, y1, w, h = cv2.boundingRect(cont)
    area = w * h

    # check if contour is high enough to be the bin
    if h > analyzedHeight * THRESHOLD_HEIGHT:
        # find center of contour
        (x, y), radius = cv2.minEnclosingCircle(cont)
        # print line from middle of board to center of detected object
        cv2.line(img2Print, (int(middle + borderX), int(borderY +y)), (int(x + borderX), int(borderY +y)), (0, 0, 255), thickness=10)
        # The gap is the distance between the detected center of the bin and the effective center
        # (some parts may be outside the analyzed area)
        gap = 0

        # check if the hole bin is on the analyzed part of the image
        if area < binMinArea:
            gap = BIN_WIDTH / 2 - w / 2
            gap = -gap if x < middle else gap

        # print line from middle of board to effectife center of object
        cv2.line(img2Print, (int(middle + borderX), int(borderY + y)), (int(x + gap + borderX),  int(borderY + y)), (0, 255, 255), thickness=5)
        lineLength = x + gap - middle
        print (lineLength)



# show the images
cv2.imshow(WINDOW_NAME, img2Print)


cv2.waitKey(0)
cv2.destroyAllWindows()

