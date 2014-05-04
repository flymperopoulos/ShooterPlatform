# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 21:29:13 2014

@author: sidd
"""

import pygame
from pygame.locals import *
import math
import numpy as np
from os import listdir
from os.path import isfile, join
import random
import numpy as np
import cv2



class Camera:
    def __init__(self, screen):
        self.cam = cv2.VideoCapture(0)
        self.x=0
        self.y=0
        self.screen = screen
        self.blue = 0
        self.green = 0
        
    def update(self):
        # Capture frame-by-frame
        ret, frame = self.cam.read()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
        
        lower_green = np.uint8([70, 50, 50])
        upper_green = np.uint8([100, 255, 255])
        # Threshold the HSV image to get only blue colors
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        green = cv2.inRange(hsv, lower_green, upper_green)
        
        moment = cv2.moments(blue)
        
        moment1 = cv2.moments(green)
        
        
        if moment1['m00'] != 0:
            self.green = len(np.where(green != 0)[0]) 
            print self.green

        if moment['m00'] != 0:
            x,y = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
            camWidth = self.cam.get(3)
            camHeight = self.cam.get(4)
            self.x = int((1.0*self.cam.get(3)-x)/camWidth*self.screen.get_size()[0])
            self.y = int((1.0*y)/camHeight*self.screen.get_size()[1])
#            print len(np.where(blue != 0)[0])
#            print len(blue)
#            self.blue = len(np.where(blue != 0)[0])
            self.blue = len(np.where(blue != 0)[0])
    
    def endCam(self):
        self.cam.release()
        cv2.destroyAllWindows()

        
class HUD:
    
    def __init__(self,screen):
        self.score = 0
        self.health = 100
        self.screen = screen
        
    def scoreUp(self):
        self.score+=1
        
    def hurt(self):
        self.health-=1
        
    def update(self):
        font = pygame.font.Font(None, 36)
        text1 = font.render("Score: " + str(self.score), 1, (10, 10, 10))
        text2 = font.render("Health: " + str(self.health), 1, (10, 10, 10))
        text3 = font.render("Gun is Empty", 1,(10, 10, 10))        
        self.screen.blit(text1,(50,50))
        self.screen.blit(text2,(725,50))
#        if self.gun.isEmpty():        
#            self.screen.blit(text,(100,100))
        
    def endGame(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.score), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = self.screen.get_rect().centery
        self.screen.blit(text, textpos)
        
class Background:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.bgImage = pygame.transform.scale(pygame.image.load('landscape.png'),self.screen.get_size())
        
    def update(self):
        
        self.screen.blit(self.bgImage,(0,0))
        
class Gun:
    
    def __init__(self,screen,cam, ammo):
        self.x = 0
        self.y = 0
        self.cam = cam
        self.screen = screen
        self.crosshair = pygame.image.load('target.png')
        self.gunSize = self.crosshair.get_size()
        self.ammo = ammo
        self.rAmmo = ammo
        
    def reloaded(self):
        self.ammo = self.rAmmo
    
    def isEmpty(self):
        if self.ammo == 0:
            return True
        return False
        
    def update(self):
        #self.x = pygame.mouse.get_pos()[0]
        #self.y = pygame.mouse.get_pos()[1]
        self.x = self.cam.x
        self.y = self.cam.y
        self.screen.blit(self.crosshair,(self.x-self.gunSize[0]/2,self.y-self.gunSize[1]/2))
        font = pygame.font.Font(None, 36)
        if self.isEmpty():
            text3 = font.render("Gun is Empty", 1,(10, 10, 10))        
            self.screen.blit(text3,(100,100))
        
        
        
class Scaler:
    
    def __init__(self, yRange, xRange1, xRange2):
        
        self.yRange = yRange
        self.xRange1 = xRange1
        self.xRange2 = xRange2
        self.scaleFactor = (1.0*((xRange2[1]-xRange2[0])-(xRange1[1]-xRange1[0])))/(yRange[1]-yRange[0])
        
    def scale(self,yVal,initWidth):
        relDist = 1.0*(yVal-self.yRange[0])/(self.yRange[1]-self.yRange[0])
        widthDist = 1.0*initWidth/(self.xRange1[1]-self.xRange1[0])
        newRoadWidth = 1.0*((self.xRange2[1]-self.xRange2[0])-(self.xRange1[1]-self.xRange1[0]))*relDist+(self.xRange1[1]-self.xRange1[0])        
        return newRoadWidth*widthDist/initWidth
        
    def findX(self,yVal,relX):
        relDist = 1.0*(yVal-self.yRange[0])/(self.yRange[1]-self.yRange[0])
        newRoadWidth = 1.0*((self.xRange2[1]-self.xRange2[0])-(self.xRange1[1]-self.xRange1[0]))*relDist+(self.xRange1[1]-self.xRange1[0])
        xValOffset = newRoadWidth*relX
        startX = (self.xRange2[0]-self.xRange1[0])*relDist+self.xRange1[0]
        return startX + xValOffset
    
class Wall:
    
    def __init__(self, screen, pos, width):
        
        self.screen = screen
        self.pos = pos
        self.height = 10
        
    def update(self,image):
        
        pass
        

class Enemy:
    
    def __init__(self, screen, pos, images, scaler):
        
        self.screen=screen
        self.pos=pos
        self.images = images
        self.scaler = scaler
#        self.health = health
        self.initWidth = 25
        self.oldDirection = 'still'
        self.direction = 'forward'
        self.walkCounter = 0
        self.wait = 10
        
    def update(self):
        self.move()
        image = self.images['front2']
        scaleFactor = self.scaler.scale(self.pos[1],self.initWidth)
        toDisplay = pygame.transform.scale(image,(int(scaleFactor*image.get_size()[0]),int(scaleFactor*image.get_size()[1])))
        self.screen.blit(toDisplay,(self.scaler.findX(self.pos[1],self.pos[0]),self.pos[1]))
        
    def move(self):
        self.pos = (self.pos[0],self.pos[1]+2)
        
    def isHit(self,pos):
        minPoint = (self.scaler.findX(self.pos[1],self.pos[0]),self.pos[1])
        scaleFactor = self.scaler.scale(self.pos[1],self.initWidth)
        if(pos[0]>minPoint[0] and pos[0]<minPoint[0]+self.initWidth*scaleFactor):
            if(pos[1]>minPoint[1] and pos[1]<minPoint[1]+self.images['front2'].get_size()[1]*scaleFactor):
                return True
        return False
        


class Main:
    
    def __init__(self):
        
        # Initialize PyGame stuff
        pygame.init()
        infoObject = pygame.display.Info()
        screenWidth,screenHeight = infoObject.current_w, infoObject.current_h
        height=int(screenHeight)
        width=int(height)
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Shooter Platform')
        self.clock=pygame.time.Clock()
        
        self.background = Background(self.screen)
        self.enemyImages = {}

        enemyFiles = [ f for f in listdir('SoldierSprite/') if isfile(join('SoldierSprite/',f)) ]
        for f in enemyFiles:
            image = pygame.image.load('SoldierSprite/'+f)
            resized = pygame.transform.scale(image,(25,int(25.0/image.get_size()[0]*image.get_size()[1])))
            self.enemyImages[f[0:-4]]=resized
            
        self.scaler = Scaler((1,600),(330,570),(28,866))
        
        self.enemies=[]
        self.newEnemyProb = .01
        
        self.cam = Camera(self.screen)
        self.gun = Gun(self.screen,self.cam, 100)
        
        self.hud = HUD(self.screen)
        

        
    def updateEnemies(self):
        if random.random()<=self.newEnemyProb:
            self.enemies.insert(0,Enemy(self.screen,(random.random(),1),self.enemyImages,self.scaler))
            self.newEnemyProb+=.001
            
        for enemy in self.enemies:
            enemy.update()
            if enemy.pos[1]>900:
                self.enemies.remove(enemy)
                self.hud.hurt()
        
    def update(self):
         # Set the FPS of the game
        self.clock.tick(60)
        
        # Clear the screen
        self.screen.fill([100,200,100])        
        
        for event in pygame.event.get():

            if event.type==QUIT:
                self.cam.endCam()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.cam.endCam()
                    exit()
                    
#                if event.key == K_SPACE:
#                    pos = (self.cam.x,self.cam.y)
#                           
#                    if self.gun.isEmpty():
#                    
#                        break
#                    else:
#                        self.gun.ammo -= 1
#                    
#                        for enemy in self.enemies[::-1]:
#                            if enemy.isHit(pos):
#                                self.enemies.remove(enemy)
#                                self.hud.scoreUp()
#                                break
                            
                            
#                if event.key == K_r:
#                    self.gun.reloaded()
            
#            if event.type == pygame.MOUSEBUTTONUP:
#                pos = pygame.mouse.get_pos()
#                
#                for enemy in self.enemies[::-1]:
#                    if enemy.isHit(pos):
#                        self.enemies.remove(enemy)
#                        self.hud.scoreUp()
#                        break
                    
        if self.hud.health>0:
            self.background.update()
            self.cam.update()
            self.updateEnemies()
            if self.cam.blue <10:
                self.gun.reloaded()
            
            if self.cam.green <60:
                pos = (self.cam.x,self.cam.y)
                       
                if self.gun.isEmpty():
                    pass
                else:
                    self.gun.ammo -= 1
                
                    for enemy in self.enemies[::-1]:
                        if enemy.isHit(pos):
                            self.enemies.remove(enemy)
                            self.hud.scoreUp()
                            break

        
            pygame.draw.line(self.screen,(100,100,200),(330,1),(570,1))
            pygame.draw.line(self.screen,(100,100,200),(28,600),(866,600))
        
            self.hud.update()
        
            self.gun.update()
        else:
            self.hud.endGame()
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Main()
    while True:
        game.update()