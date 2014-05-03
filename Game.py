# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 21:29:13 2014

@author: 
Sidd Singal
James Jang
Filippos Lymperopoulos
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
        
    def update(self):
        # Capture frame-by-frame
        ret, frame = self.cam.read()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
        # Threshold the HSV image to get only blue colors
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        moment = cv2.moments(blue)
        
        if moment['m00'] != 0:
            x,y = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
            camWidth = self.cam.get(3)
            camHeight = self.cam.get(4)
            self.x = int((1.0*self.cam.get(3)-x)/camWidth*self.screen.get_size()[0])
            self.y = int((1.0*y)/camHeight*self.screen.get_size()[1])
    
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
        self.screen.blit(text2,(self.screen.get_size()[0]-150,50))
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
        
    def scale(self,yVal,initWidth):
        wScaled=(self.xRange2[1]-self.xRange2[0])*initWidth/(self.xRange1[1]-self.xRange1[0])
        relY = yVal*1.0/(self.yRange[1]-self.yRange[0])
        newWidth = (wScaled-initWidth)*relY+initWidth
        return newWidth/initWidth
        
    def findX(self,yVal,relX):
        relDist = 1.0*(yVal-self.yRange[0])/(self.yRange[1]-self.yRange[0])
        newRoadWidth = 1.0*((self.xRange2[1]-self.xRange2[0])-(self.xRange1[1]-self.xRange1[0]))*relDist+(self.xRange1[1]-self.xRange1[0])
        xValOffset = newRoadWidth*relX
        startX = (self.xRange2[0]-self.xRange1[0])*relDist+self.xRange1[0]
        return startX + xValOffset
    
class Wall:
    
    def __init__(self, screen, pos, height):
        
        self.screen = screen
        self.pos = pos
        self.height = height
        self.width = 2*self.height
        
    def update(self):
        pygame.draw.rect(self.screen,(250,0,0),Rect((int(self.pos[0]-self.width/2.0),int(self.pos[1]-self.height)),((int(self.pos[0]+self.width/2.0),int(self.pos[1])))))
  
class EnemyManager:
    def __init__(self,screen,scaler,hud):
        self.screen = screen
        self.hud = hud
        self.enemies = []
        self.walls = []
        self.newEnemyProb = .01
        self.enemyImages = {}
        self.scaler = scaler
        self.walls.append(Wall(self.screen,(100,100),20))

        enemyFiles = [ f for f in listdir('SoldierSprite/') if isfile(join('SoldierSprite/',f)) ]
        for f in enemyFiles:
            image = pygame.image.load('SoldierSprite/'+f)
            resized = pygame.transform.scale(image,(25,int(25.0/image.get_size()[0]*image.get_size()[1])))
            self.enemyImages[f[0:-4]]=resized
        
    def updateEnemies(self):
        if random.random()<=self.newEnemyProb:
            self.enemies.insert(0,Enemy(self.screen,(random.random(),1),self.enemyImages,self.scaler))
            self.newEnemyProb+=.001
            
        for enemy in self.enemies:
            enemy.update()
            if enemy.pos[1]>900:
                self.enemies.remove(enemy)
                self.hud.hurt()

    def checkHit(self,pos):
        for enemy in self.enemies[::-1]:
            if enemy.isHit(pos):
                self.enemies.remove(enemy)
                self.hud.scoreUp()
                break

    def createWalls(self):
        pass

    def update(self):
        self.updateEnemies()

        for wall in self.walls:
            wall.update()

class Enemy:
    
    def __init__(self, screen, pos, images, scaler):
        
        self.screen=screen
        self.pos=pos
        self.images = images
        self.scaler = scaler
#       self.health = health
        self.initWidth = 25.0
        self.initSpeed = 2.0
        self.oldDirection = 'still'
        self.direction = 'forward'
        self.walkCounter = 0
        self.wait = 10 
        self.speed = 1

        # self.soundPlayed = False
    
    def update(self):
        self.move()
        image = self.images['front2']
        scaleFactor = self.scaler.scale(self.pos[1],self.initWidth)
        toDisplay = pygame.transform.scale(image,(int(scaleFactor*image.get_size()[0]),int(scaleFactor*image.get_size()[1])))
        self.screen.blit(toDisplay,(self.scaler.findX(self.pos[1],self.pos[0]),self.pos[1]))
        
    def move(self):
        speed = .2*(self.initSpeed*self.scaler.scale(self.pos[1],self.initSpeed))**2
        self.pos = (self.pos[0],self.pos[1]+speed)
        
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
        self.shooting = False
        
        self.background = Background(self.screen)
        
        size = self.screen.get_size()
        self.scaler = Scaler((1/900.0*size[1],600/900.0*size[1]),(330/900.0*size[0],570/900.0*size[0]),(28/900.0*size[0],866/900.0*size[0]))
                
        self.cam = Camera(self.screen)
        self.gun = Gun(self.screen,self.cam, 7)
        
        self.hud = HUD(self.screen)
        self.enMan = EnemyManager(self.screen,self.scaler,self.hud)

                
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
                    
                if event.key == K_SPACE:
                    # self.soundPlayed = True       
                    pos = (self.cam.x,self.cam.y)
                    if self.gun.isEmpty():
                        break
                    else:
                        self.gun.ammo -= 1
                        self.shooting = True
                        self.enMan.checkHit(pos)
                        self.track = pygame.mixer.music.load('shot.wav') 
                        pygame.mixer.music.play()
                if event.key == K_r:
                    self.gun.reloaded()
                    self.track = pygame.mixer.music.load('reloadFinal.wav')        
                    pygame.mixer.music.play()
                    
            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     for enemy in self.enemies[::-1]:
            #         if enemy.isHit(pos):
            #             self.enemies.remove(enemy)
            #             self.hud.scoreUp()
            #             break

        if self.hud.health>0:
            self.background.update()
            self.cam.update()
            self.enMan.update()

            size = self.screen.get_size()
            pygame.draw.line(self.screen,(100,100,200),(330/900.0*size[0],1/900.0*size[1]),(570/900.0*size[0],1/900.0*size[1]))
            pygame.draw.line(self.screen,(100,100,200),(28/900.0*size[0],600/900.0*size[1]),(866/900.0*size[0],600/900.0*size[1]))
        
            self.hud.update()
        
            self.gun.update()
            if self.shooting:
                s = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill((255,255,255))           # this fills the entire surface
                self.screen.blit(s, (0,0)) 
                self.shooting = False
        else:
            self.hud.endGame()
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Main()
    while True:
        game.update()
