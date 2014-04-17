# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 22:33:33 2014

@author: james
"""

import numpy as np
import cv2

class shooting:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cam = cv2.VideoCapture(0)
        ret, self.frame = cam.read()    
        
    def update(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
        moment = cv2.moments(blue)
        if moment['m00'] != 0:
            x,y = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
        
        self.x = int(cam.get(3))-x
        self.y = y
    
    def endCam(self):
        self.cam.release()
        
class gun:
    def __init__(self):

        
    def update(self, x,y):        
        self.x = x
        self.y = y