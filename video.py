# -*- coding: utf-8 -*-

import numpy as np
import cv2

cam = cv2.VideoCapture(0)
print cam.get(3)
print cam.get(4)

green = np.uint8([[[0,0,255]]]) 
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print hsv_green

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    # different kinds of frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
#   hsv_frame = cv2.createImage(cv2.GetSize(frame), 8, 3)

    # define range of blue color in HSV
    lower_blue = np.uint8([110, 50, 50])
    upper_blue = np.uint8([130,255,255])

    # define range of green color in HSV
 

    lower_red= np.uint8([10, 255, 50])
    upper_red = np.uint8([40, 255, 255])

    # Threshold the HSV image to get only blue colors
    blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    green = cv2.inRange(hsv, lower_green, upper_green)
    
    red = cv2.inRange(hsv, lower_red, upper_red)

    moment = cv2.moments(blue)
    
    moment1 = cv2.moments(green)
    
    moment2 = cv2.moments(green)

    if moment['m00'] != 0:
        bx,by = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
#        pxrint moment['m10']
#        print moment['m00']
#        print moment['m01']
        
#        cv2.circle(blue,(int(cam.get(3))-bx,by),30,255,-1)

    # Added reflection on screen for color detection.
    if moment1['m00'] != 0:
        gx,gy = int(moment1['m10']/moment1['m00']), int(moment1['m01']/moment1['m00'])
        print len(np.where(green != 0)[0])
#        cv2.circle (green,(int(cam.get(3))-gx,gy),50,255,-1)
#    
#    if moment2['m00'] != 0:
#        x,y = int(moment2['m10']/moment2['m00']), int(moment2['m01']/moment2['m00'])
#        cv2.circle (red,(int(cam.get(3))-x,y),50,255,-1)
#    print bx, by
#    print gx, gy
#    if abs(bx - gx )< 1 and abs(by - gy )< 1:
#        cv2.circle(blue,(int(cam.get(3))-gx,gy),50,255,-1)
    
#    print blue
#    print blue[0]

#    print len(np.where(blue != 0)[0])
#    
    cv2.imshow('video',frame)
       
    cv2.imshow('only blue',blue)
    
    cv2.imshow('some red', red)

    cv2.imshow('some green', green) 

    
    # Display the resulting frame
#    cv2.imshow('frame',frame)  
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()