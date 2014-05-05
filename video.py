# -*- coding: utf-8 -*-

import numpy as np 
import cv2
#
#cam1 = cv2.VideoCapture(0)
#realgreen = 0
#realblue = 0
#i = 0
#while i < 100:
#    ret, frame = cam1.read()
#    lower_green = np.uint8([60, 60, 60])
#    upper_green = np.uint8([90, 255, 255])
#    lower_blue = np.uint8([110, 100, 100])
#    upper_blue = np.uint8([130,255,255])
#    
#    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#    green = cv2.inRange(hsv, lower_green, upper_green)
#    blue = cv2.inRange(hsv, lower_blue, upper_blue)
#    
#    realgreen += green
#    realblue += blue
#    
#    
##    if cv2.waitKey(1) & 0xFF == ord(' '):
##        realgreen[np.where(realgreen != 0)] = 255
##        cv2.imwrite('initalgreen.png', realgreen)
##        realgreen = cv2.imread('initalgreen.png', 0)
##        
##        realblue[np.where(realblue != 0)] = 255
##        cv2.imwrite('initalblue.png', blue)
##        backblue = cv2.imread('initalgreen.png', 0)
##        break
#    i+= 1
#realgreen[np.where(realgreen != 0)] = 255
#cv2.imwrite('initalgreen.png', realgreen)
#realgreen = cv2.imread('initalgreen.png', 0)
#
#realblue[np.where(realblue != 0)] = 255
#cv2.imwrite('initalblue.png', blue)
#backblue = cv2.imread('initalgreen.png', 0)
#
#cam1.release()
#cv2.destroyAllWindows()

cam = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    # different kinds of frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_blue = np.uint8([110, 100, 100])
    upper_blue = np.uint8([130,255,255])

    # define range of green color in HSV
    lower_green = np.uint8([40, 110, 110])
    upper_green = np.uint8([70, 255, 255])

#   lower_green = np.uint8([60, 60, 60])
#   upper_green = np.uint8([90, 255, 255])

    lower_red= np.uint8([10, 255, 50])
    upper_red = np.uint8([40, 255, 255])

    blue = cv2.inRange(hsv, lower_blue, upper_blue)
    green = cv2.inRange(hsv, lower_green, upper_green)    
    red = cv2.inRange(hsv, lower_red, upper_red)
    
    
    
#    green = green - realgreen
#    blue = blue - realblue
    print len(np.where(green != 0)[0])
    moment = cv2.moments(blue)
    moment1 = cv2.moments(green)

    if moment['m00'] != 0:
        bx,by = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
#        cv2.circle(blue,(int(cam.get(3))-bx,by),30,255,-1)
    if moment1['m00'] != 0:
        gx,gy = int(moment1['m10']/moment1['m00']), int(moment1['m01']/moment1['m00'])
#        print len(np.where(green != 0)[0])
#        cv2.circle (green,(int(cam.get(3))-gx,gy),50,255,-1)
#    
#    if moment2['m00'] != 0:
#        x,y = int(moment2['m10']/moment2['m00']), int(moment2['m01']/moment2['m00'])
#        cv2.circle (red,(int(cam.get(3))-x,y),50,255,-1)
#    print bx, by
#    print gx, gy
 
    cv2.imshow('video',frame)
#    cv2.imshow('only blue',blue)
#    cv2.imshow('some red', red)
    cv2.imshow('some green', green)
#    cv2.imshow('backgreen', realgreen)
#    cv2.imshow('backblue', realblue)
    
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
    
# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()