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
scaleFactor = 0.4

# Bin width = 500px -> declare as max
# Bin width on left or right side is +/- 300px
binRectangleAreaMin = 300 * 250 * scaleFactor
binRectangleAreaMax = 500 * 250 * scaleFactor




# define on change method
def on_change(position):
    pass

#define trackbar
cv2.createTrackbar('Threshold Value', 'window', threshold_value, threshold_maxvalue, on_change)


if __name__ == '__main__':
    # capture video from camera

    # Take each frame
    while True:

        image = cv2.imread('right.jpg')
        resizeImage = cv2.resize(image, (0, 0), fx=scaleFactor, fy=scaleFactor)
        cropImage = image[1200:1450, 350:2242]
        processingImage = cv2.resize(cropImage, (0, 0), fx=scaleFactor, fy=scaleFactor)
     #   frame = cv2.resize(image, (0,0), fx=0.3, fy=0.3)

        # convert to greyscale
        bw_image = cv2.cvtColor(processingImage, cv2.COLOR_BGR2GRAY)

        # invert picture
        wb_image = cv2.bitwise_not(bw_image)
        wb2_image = wb_image.copy()

        # create binary picture
        ret, binaryImage1 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, binaryImage2 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, binaryImage3 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)

        # filtering
        kernel = np.ones((8, 8), np.uint8)
        filteredBinaryImage = cv2.morphologyEx(binaryImage3, cv2.MORPH_OPEN, kernel)
        filteredBinaryImage2 = filteredBinaryImage.copy()



        contours2, hierarchy2 = cv2.findContours(filteredBinaryImage2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours2:
            #print("array")
            #print(cnt)

            #cv2.circle(frame, (cnt[0], cnt[1]), 3, (0, 255, 0), -1)
            contourArea = cv2.contourArea(cnt)
         #   print(contourArea)
         #   print(binRectangleAreaMin)
         #   print(binRectangleAreaMax)
            if 5000 < contourArea < 20000:
            #    print(contourArea)
                cv2.drawContours(processingImage, [cnt], 0, (0, 255, 0), 2)

                hull = cv2.convexHull(cnt)
                print(hull)

                for points in hull:

                    point = points[0]
                    print(point[0], point[1])
                    cv2.circle(processingImage, (point[0], point[1]), 5, (0, 0, 255))


                # get centroid
                M = cv2.moments(cnt)
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                cv2.circle(processingImage, (centroid_x, centroid_y), 3, (0, 150, 0))
                print(centroid_x)

        #for cnt in contours2:
        #    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        #    cv2.drawContours(frame ,[cnt], -1, (0, 255, 0), 2)

     #   cv2.imshow('crop', crop_img);
        cv2.imshow('crop', processingImage)
        cv2.imshow('original', resizeImage)
     #   cv2.imshow('original', image)
        cv2.imshow('contours (opening2)', filteredBinaryImage2)
        cv2.imshow('binary (binaryImage2)', binaryImage2)
        cv2.imshow('after filter (opening)', filteredBinaryImage)
    #    cv2.imshow('hsv mask', hsv_opening)
        #print(contours2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

    cv2.waitKey(0)
    cv2.destroyAllWindows()