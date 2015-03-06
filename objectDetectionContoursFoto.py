__author__ = 'orceN'


import cv2
import numpy as np

# define window
cv2.namedWindow('window')

# define variable
threshold_value = 0
threshold_maxvalue = 255
threshold_maxval_180 = 180
red = (0, 0, 255, 0)

# origin image is too big, defines a scalefactor to smaller the picture
scaleFactor = 1

# Bin width = 500px -> declare as max
# Bin width on left or right side is +/- 300px
binRectangleAreaMin = 300 * 250 * scaleFactor
binRectangleAreaMax = 500 * 250 * scaleFactor

# Centroids
pictureCentroidX = 0
pictureCentroidY = 0
contourCentroidX = 0
contourCentroidY = 0




# define on change method
def on_change(position):
    pass

#define trackbar
cv2.createTrackbar('Threshold Value', 'window', threshold_value, threshold_maxvalue, on_change)


if __name__ == '__main__':
    # capture video from camera

    # Take each frame
    while True:

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
        ret, binaryImage1 = cv2.threshold(processingGreyInvCopy, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, binaryImage2 = cv2.threshold(processingGreyInvCopy, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, binaryImage3 = cv2.threshold(processingGreyInvCopy, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)

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
            print(fullCentroidX)
            pictureCentroidX = fullCentroidX
            pictureCentroidY = fullCentroidY

        # evaluate contours on picture -> find bin
        contours2, hierarchy2 = cv2.findContours(filteredBinaryImage2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours2:
            contourArea = cv2.contourArea(cnt)
            if binRectangleAreaMin < contourArea < binRectangleAreaMax:

                cv2.drawContours(processingImage, [cnt], 0, (0, 255, 0), 2)

                # find and draw endpoints of contour
                hull = cv2.convexHull(cnt)
                for points in hull:
                    point = points[0]
                    cv2.circle(processingImage, (point[0], point[1]), 5, (0, 0, 255))

                # get centroid of contour
                contourMoments = cv2.moments(cnt)
                centroidX = int(contourMoments['m10']/contourMoments['m00'])
                centroidY = int(contourMoments['m01']/contourMoments['m00'])
                cv2.circle(processingImage, (centroidX, centroidY), 3, (0, 150, 0))
                print(centroidX)
                contourCentroidX = centroidX
                contourCentroidY = centroidY

        #calculate difference to picture centroid
        if not (pictureCentroidX is None):
            if not (contourCentroidX is None):
                distanceToCentroid = pictureCentroidX - contourCentroidX
                print(distanceToCentroid)

                cv2.line(referenceImage, (pictureCentroidX, pictureCentroidY), (contourCentroidX, contourCentroidY), (0, 0, 255), 2)

        cv2.imshow('crop', processingImage)
        cv2.imshow('contours (opening2)', filteredBinaryImage2)
        cv2.imshow('binary (binaryImage2)', binaryImage2)
        cv2.imshow('after filter (opening)', filteredBinaryImage)
        cv2.imshow('fullBinary', referenceImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()