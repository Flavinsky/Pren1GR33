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
#cv2.createTrackbar('B_lower_H', 'window', threshold_value, threshold_maxval_180, on_change)
#cv2.createTrackbar('B_lower_S', 'window', threshold_value, threshold_maxvalue, on_change)
#cv2.createTrackbar('B_lower_V', 'window', threshold_value, threshold_maxvalue, on_change)
#cv2.createTrackbar('B_up_H', 'window', threshold_value, threshold_maxval_180, on_change)
#cv2.createTrackbar('B_up_S', 'window', threshold_value, threshold_maxvalue, on_change)
#cv2.createTrackbar('B_up_V', 'window', threshold_value, threshold_maxvalue, on_change)


if __name__ == '__main__':
    # capture video from camera

    # Take each frame
    while True:

        image = cv2.imread('middle.jpg')
        resizeImage = cv2.resize(image, (0, 0), fx=scaleFactor, fy=scaleFactor)
        crop_img = image[1200:1450, 350:2242]
        frame = cv2.resize(crop_img, (0, 0), fx=scaleFactor, fy=scaleFactor)
     #   frame = cv2.resize(image, (0,0), fx=0.3, fy=0.3)



        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # background_lower
     #   brown_low = np.array([cv2.getTrackbarPos('B_lower_H', 'window'), cv2.getTrackbarPos('B_lower_S', 'window'), cv2.getTrackbarPos('B_lower_V', 'window')])
     #   brown_up = np.array([cv2.getTrackbarPos('B_up_H', 'window'), cv2.getTrackbarPos('B_up_S', 'window'), cv2.getTrackbarPos('B_up_V', 'window')])

     #   mask = cv2.inRange(hsv, brown_low, brown_up)

      #  kernel = np.ones((4, 4), np.uint8)
     #   hsv_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)



        # convert to greyscale
        bw_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # invert picture
        wb_image = cv2.bitwise_not(bw_image)
        wb2_image = wb_image.copy()

        # create binary picture
        ret, thresh2 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, thresh3 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)
        ret, thresh4 = cv2.threshold(wb2_image, cv2.getTrackbarPos('Threshold Value', 'window'), 255, cv2.THRESH_BINARY)

        # filtering
        kernel = np.ones((8, 8), np.uint8)
        opening = cv2.morphologyEx(thresh4, cv2.MORPH_OPEN, kernel)
        opening2 = opening.copy()



        contours2, hierarchy2 = cv2.findContours(opening2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #Draw a contour points
        #for (x,y) in contours2:
        #   cv2.circle(thresh2, (x,y), 2, red)
        # print(contours2)

        for cnt in contours2:
            print("array")
            print(cnt)

            M = cv2.moments(cnt)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

            cv2.circle(frame, (centroid_x, centroid_y), 3, (0, 150, 0))

            #cv2.circle(frame, (cnt[0], cnt[1]), 3, (0, 255, 0), -1)
            contourArea = cv2.contourArea(cnt)
            if 8000 < contourArea < 20000:
            #    print(contourArea)
                cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)

        #for cnt in contours2:
        #    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        #    cv2.drawContours(frame ,[cnt], -1, (0, 255, 0), 2)

     #   cv2.imshow('crop', crop_img);
        cv2.imshow('crop', frame)
        cv2.imshow('original', resizeImage)
        cv2.imshow('contours', opening2)
        cv2.imshow('window', thresh3)
        cv2.imshow('after filter', opening)
    #    cv2.imshow('hsv mask', hsv_opening)
        #print(contours2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

    cv2.waitKey(0)
    cv2.destroyAllWindows()