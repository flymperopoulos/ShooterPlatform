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
import time

class Camera:
    def __init__(self, screen):
        self.cam = cv2.VideoCapture(0)
        self.x=0
        self.y=0
        self.screen = screen
        self.blue = 0
        self.green = 0
        self.realgreen = 0
        self.realblue = 0
    
    def calibrate(self):
        ret, frame = self.cam.read()
#        
#        lower_green = np.uint8([60, 60, 60])
#        upper_green = np.uint8([90, 255, 255])

        lower_green = np.uint8([40, 100, 100])
        upper_green = np.uint8([70, 255, 255])
        
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        green = cv2.inRange(hsv, lower_green, upper_green)
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        self.realgreen += green
        self.realblue += blue
    
    def endCalibration(self):
        self.realgreen[np.where(self.realgreen != 0)] = 255
        cv2.imwrite('initalgreen.png', self.realgreen)
        self.realgreen = cv2.imread('initalgreen.png', 0)
            
        self.realblue[np.where(self.realblue != 0)] = 255
        cv2.imwrite('initalblue.png', self.realblue)
        self.realblue = cv2.imread('initalgreen.png', 0)
#        print len(np.where(self.realblue == 255))
        cv2.destroyAllWindows()
        
    def update(self):
        # Capture frame-by-frame
        ret, frame = self.cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
            
#        lower_green = np.uint8([60, 60, 60])
#        upper_green = np.uint8([90, 255, 255])

        lower_green = np.uint8([40, 100, 100])
        upper_green = np.uint8([70, 255, 255])
        
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        green = cv2.inRange(hsv, lower_green, upper_green)
    
#        green = green - self.realgreen
#        blue = blue - self.realblue
        
        moment = cv2.moments(blue)
        
        moment1 = cv2.moments(green) 
        
#        if moment1['m00'] != 0:
        self.green = len(np.where(green != 0)[0])
#        print self.green

        if moment['m00'] != 0:
            x,y = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
            camWidth = self.cam.get(3)
            camHeight = self.cam.get(4)
            self.x = int((1.0*self.cam.get(3)-x)/camWidth*self.screen.get_size()[0])
            self.y = int((1.0*y)/camHeight*self.screen.get_size()[1])
            self.blue = len(np.where(blue == 255)[0])
            
    
    def endCam(self):
        self.cam.release()
        cv2.destroyAllWindows()

        
class HUD:
    
    def __init__(self,screen):
        self.score = 0
        self.maxHealth = 100
        self.health = self.maxHealth
        self.screen = screen
        self.font = pygame.font.SysFont("Comic Sans MS", self.screen.get_size()[1]/30)

    def scoreUp(self):
        self.score+=1
        
    def hurt(self):
        self.health-=10
        hurtEnem = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  
        hurtEnem.set_alpha(100)                
        hurtEnem.fill((239,66,66))           
        self.screen.blit(hurtEnem, (0,0)) 


    def shot(self):
        self.health-=1
        hurtEnem = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  
        hurtEnem.set_alpha(100)                
        hurtEnem.fill((239,66,66))           
        self.screen.blit(hurtEnem, (0,0)) 
        
    def update(self):
        pygame.draw.rect(self.screen, (255,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/4.5,self.screen.get_size()[1]/25), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/70)))
        pygame.draw.rect(self.screen, (103,171,216), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/4.5,self.screen.get_size()[1]/24), ((self.screen.get_size()[0]/5)*1.0*self.health/self.maxHealth,self.screen.get_size()[1]/90)))        
        text1 = self.font.render("Score: " + str(self.score), 1, (10, 10, 10))
        text2 = self.font.render("Health: " + str(100/self.maxHealth*self.health) + '%', 1, (10, 10, 10))
        text3 = self.font.render("Gun is Empty", 1,(10, 10, 10))        
        self.screen.blit(text1,(self.screen.get_size()[0]/12,self.screen.get_size()[1]/13))
        self.screen.blit(text2,(self.screen.get_size()[0]-self.screen.get_size()[0]/5.1,self.screen.get_size()[1]/17))
#       if self.gun.isEmpty():        
#           self.screen.blit(text,(100,100))
        
    def endGame(self):
        text = self.font.render("Score: " + str(self.score), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = self.screen.get_rect().centery
        self.screen.blit(text, textpos)

    def pauseGame(self):
        text = self.font.render("Continue",1, (10, 10, 10))
        pygame.draw.rect(self.screen, (255,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/1.68,self.screen.get_size()[1]/2.5), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/10)))
        # image = pygame.Surface([640,480], pygame.SRCALPHA, 32)
        # image = image.convert_alpha()
        self.screen.blit(text,(self.screen.get_size()[0]/2.2,self.screen.get_size()[1]/2.3))
        # self.screen.blit(image,(self.screen.get_size()[0]/2.2,self.screen.get_size()[1]/2.3))
        
class Background:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.bgImage = pygame.transform.scale(pygame.image.load('landscape.png'),self.screen.get_size())
        
    def update(self):
        
        self.screen.blit(self.bgImage,(0,0))
        
class Gun(object):
    
    def __init__(self,screen,cam, ammo):
        self.x = 0
        self.y = 0 
        self.cam = cam
        self.screen = screen
        self.crosshair = pygame.image.load('target.png')
        self.gunSize = self.crosshair.get_size()
        self.ammo = ammo
        self.rAmmo = ammo
        self.bullet = pygame.image.load('bullet.png').convert_alpha()
        self.bulletShow = True
        self.font = pygame.font.SysFont("Comic Sans MS", self.screen.get_size()[1]/30)
        self.hitRadius = self.screen.get_size()[1]/100
        self.numShot =1
        
    def reloaded(self):
        self.ammo = self.rAmmo

    def isEmpty(self):
        if self.ammo == 0:
            return True
        return False
        
    def update(self):
        #self.x = pygame.mouse.get_pos()[0]
        #self.y = pygame.mouse.get_pos()[1]
        if self.bulletShow:
            for i in range(1,self.ammo+1):
                toShow = pygame.transform.scale(self.bullet, (int(0.3*(self.bullet.get_size()[0])), int(0.3*(self.bullet.get_size()[1]))))
                self.screen.blit(toShow,(self.screen.get_size()[0]/30*i,self.screen.get_size()[1]/35))
            if self.isEmpty():

                text3 = self.font.render("Gun is Empty", 1,(240, 10, 10))        
                self.screen.blit(text3,(self.screen.blit(text3,(self.screen.get_size()[0]/16,self.screen.get_size()[1]/25))))

        self.x = self.cam.x
        self.y = self.cam.y
        self.screen.blit(self.crosshair,(self.x-self.gunSize[0]/2,self.y-self.gunSize[1]/2))       

class Shotgun(Gun):
    def __init__(self,screen,cam, ammo):
        super(Shotgun, self).__init__(screen, cam, ammo)
        self.hitRadius = self.screen.get_size()[1]/20
        self.numShot = 25
        self.crosshair = pygame.transform.scale2x(pygame.image.load('target.png'))
        
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
    
    def __init__(self, screen, pos, width, height):
        
        self.screen = screen
        self.pos = pos
        self.height = height
        self.width = width
        
    def isHit(self,pos):
        
        if pos[0]<self.pos[0]-self.width/2 or pos[0]>self.pos[0]+self.width/2:
            return False
        elif pos[1]<self.pos[1]-self.height or pos[1]>self.pos[1]:
            return False
        else:
            return True
        
    def update(self):
        pygame.draw.rect(self.screen,(100,100,100),Rect((int(self.pos[0]-self.width/2.0),int(self.pos[1]-self.height)),((int(self.width),int(self.height)))))
        
  
class WallRow:
    
    def __init__(self,screen,yPos,height,scaler,edged, gapWidth, numGaps, last):
        
        self.screen = screen
        self.yPos = yPos
        self.height=height
        self.scaler=scaler
        self.edged = edged
        self.gapWidth = gapWidth
        self.numGaps = numGaps
        self.last = last
        
        
        if edged:
            self.positions = range(numGaps*2)
        else:
            self.positions = range((numGaps-1)*2)
        self.xCovers = []
        self.xExits = []
        self.yCover = yPos - height*.2
        roadWidth = scaler.scale(yPos,scaler.xRange1[1]-scaler.xRange1[0])*(scaler.xRange1[1]-scaler.xRange1[0])
        walls = 0
        if edged:
            walls = numGaps + 1
        else:
            walls = numGaps - 1
            
        wallWidth = (roadWidth - numGaps*gapWidth)/walls
        
        self.walls = []
        xInit = self.scaler.findX(self.yPos,0)
        if edged:
            for i in range(numGaps+1):
                xPos = i*wallWidth+i*gapWidth+wallWidth/2+xInit
                self.walls.append(Wall(self.screen,(xPos,self.yPos),wallWidth, self.height))
                roadBeginning = self.scaler.findX(yPos,0)
                if i==0:
                    self.xCovers.append((xPos+wallWidth/4.0-roadBeginning)/roadWidth)
                    self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-roadBeginning)/roadWidth)
                elif i==numGaps:
                    self.xCovers.append((xPos-wallWidth/4.0-roadBeginning)/roadWidth)
                    self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-roadBeginning)/roadWidth)
                else:
                    self.xCovers.append((xPos-wallWidth/4.0-roadBeginning)/roadWidth)
                    self.xCovers.append((xPos+wallWidth/4.0-roadBeginning)/roadWidth)
                    self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-roadBeginning)/roadWidth)
                    self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-roadBeginning)/roadWidth)
        else:
            for i in range(numGaps-1):
                roadBeginning = self.scaler.findX(yPos,0)
                xPos = i*wallWidth+i*gapWidth+wallWidth/2+gapWidth+xInit
                self.walls.append(Wall(self.screen,(xPos,self.yPos),wallWidth, self.height))
                self.xCovers.append((xPos-wallWidth/4.0-roadBeginning)/roadWidth)
                self.xCovers.append((xPos+wallWidth/4.0-roadBeginning)/roadWidth)
                self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-roadBeginning)/roadWidth)
                self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-roadBeginning)/roadWidth)
                
    def isHit(self,pos):
        
        for wall in self.walls:
            if wall.isHit(pos):
                return True
        return False
        
    def update(self):
        for wall in self.walls:
            wall.update()
            

class EnemyManager:
    
    def __init__(self,screen,scaler,hud, initWallHeight, initGapWidth):
        self.screen = screen
        self.hud = hud
        self.enemies = []
        self.wallRows = []
        self.newEnemyProb = .01
        self.enemyImages = {}
        self.scaler = scaler
        self.initWallHeight = initWallHeight
        self.initGapWidth = initGapWidth

        enemyFiles = [ f for f in listdir('SoldierSprite/') if isfile(join('SoldierSprite/',f)) ]
        for f in enemyFiles:
            image = pygame.image.load('SoldierSprite/'+f)
            resized = pygame.transform.scale(image,(25,int(25.0/image.get_size()[0]*image.get_size()[1])))
            self.enemyImages[f[0:-4]]=resized
            
        self.createWalls(5,.1,.9)
        
    def checkHit(self,pos):
        self.enemies = sorted(self.enemies, key=lambda enemy: enemy.pos[1])
        minY = 0;
        for wallRow in self.wallRows:
            if wallRow.isHit(pos):
                minY = wallRow.yPos
        print minY
        for enemy in self.enemies[::-1]:
            if enemy.isHit(pos) and enemy.pos[1]>minY:
                self.enemies.remove(enemy)
                self.hud.scoreUp()
                break

    def createWalls(self, rows, minRelY, maxRelY):
        edged = False
        gaps = 3
        gapTemp = 0
        
        for i in range(rows):
            yTemp = (i*1.0/rows)**1.5
            yRange = maxRelY-minRelY
            yPos = (yTemp*yRange+minRelY)*self.screen.get_size()[1]
            gapWidth = self.scaler.scale(yPos,self.initGapWidth)*self.initGapWidth
            height = self.scaler.scale(yPos,self.initWallHeight)*self.initWallHeight
            self.wallRows.append(WallRow(self.screen,yPos,height,self.scaler,edged,gapWidth,gaps-gapTemp,False))
            edged = not edged
            gapTemp = 1-gapTemp
            
        self.wallRows[-1].last=True

    def update(self):
        
        if random.random()<=self.newEnemyProb:
            index = random.randint(0,len(self.wallRows[0].xCovers)-1)
            pos = self.wallRows[0].xCovers[index]
            newEnemy = Enemy(self.screen,(pos,1),index,0,self.enemyImages,self.scaler)
            newEnemy.updateQueue([['forward',self.wallRows[0].yCover]])
            self.enemies.insert(0,newEnemy)
            self.newEnemyProb+=.001
        
                    
        for enemy in self.enemies:
            if enemy.status =='available':
                shootProb = .2
                waitProb = .3
                advanceProb = .5
                choice = random.random()
                if choice < shootProb:
                    enemy.updateQueue(self.sendShoot(self.wallRows[enemy.level], enemy.relPos, 3.0))
                elif choice < shootProb + waitProb:
                    enemy.updateQueue(self.makeWait(3.0))
                elif choice < shootProb + waitProb + advanceProb:
                    if not self.wallRows[enemy.level].last:
                        index = random.randint(0,len(self.wallRows[enemy.level+1].xCovers)-1)
                        pos = self.wallRows[enemy.level+1].xCovers[index]
                        enemy.updateQueue(self.getPath(self.wallRows[enemy.level],enemy.relPos,self.wallRows[enemy.level+1],index))
                        enemy.updatePosition(index,enemy.level+1)                
                    else:
                        enemy.updateQueue(self.getPath(self.wallRows[enemy.level],enemy.relPos,None,None))
                    
        for enemy in self.enemies:
            if enemy.hurtUser:
                enemy.hurtUser = False
                self.hud.shot()
            if enemy.pos[1]>self.screen.get_size()[0]:
                self.enemies.remove(enemy)
                self.hud.hurt()
                
        self.enemies = sorted(self.enemies, key=lambda enemy: enemy.pos[1])
                
        entities = len(self.wallRows)+len(self.enemies)
        wrCounter = 0
        enemyCounter = 0
        while enemyCounter + wrCounter < entities:
            if enemyCounter == len(self.enemies):
                for i in range(wrCounter,len(self.wallRows)):
                    self.wallRows[i].update()
                    wrCounter=len(self.wallRows)
            elif wrCounter == len(self.wallRows):
                for i in range(enemyCounter,len(self.enemies)):
                    self.enemies[i].update()
                    enemyCounter=len(self.enemies)
            else:
                wallY = self.wallRows[wrCounter].yPos
                enemyY = self.enemies[enemyCounter].pos[1]
                if enemyY>wallY:
                    self.wallRows[wrCounter].update()
                    wrCounter+=1
                else:
                    self.enemies[enemyCounter].update()
                    enemyCounter+=1
                
    def getPath(self, wallRowOld, wallRowOldPos, wallRowNew, wallRowNewPos):
        
        directions = []

        if wallRowOld.edged:
            if wallRowOldPos%2==0:
                directions.append(['right',wallRowOld.xExits[wallRowOldPos]])
            else:
                directions.append(['left',wallRowOld.xExits[wallRowOldPos]])
        else:
            if wallRowOldPos%2==0:
                directions.append(['left',wallRowOld.xExits[wallRowOldPos]])
            else:
                directions.append(['right',wallRowOld.xExits[wallRowOldPos]])
                
        if wallRowOld.last:
            directions.append(['forward',self.screen.get_size()[1]+100])
        else:
            directions.append(['forward',wallRowNew.yCover])
            lastDir = 'left'
            if wallRowOld.xExits[wallRowOldPos] < wallRowNew.xCovers[wallRowNewPos]:
                lastDir = 'right'
                
            directions.append([lastDir,wallRowNew.xCovers[wallRowNewPos]])
        #print 'Directions',directions
        return directions
        
    def sendShoot(self, wallRowOld, wallRowOldPos, time):
        
        directions = []
        
        if wallRowOld.edged:
            if wallRowOldPos%2==0:
                directions.append(['right',wallRowOld.xExits[wallRowOldPos]])
            else:
                directions.append(['left',wallRowOld.xExits[wallRowOldPos]])
        else:
            if wallRowOldPos%2==0:
                directions.append(['left',wallRowOld.xExits[wallRowOldPos]])
            else:
                directions.append(['right',wallRowOld.xExits[wallRowOldPos]])
                
        
        directions.append(['shoot',time])
        
        if directions[0][0] == 'left':
            directions.append(['right',wallRowOld.xCovers[wallRowOldPos]])
        else:
            directions.append(['left',wallRowOld.xCovers[wallRowOldPos]])
            
        return directions
        
    def makeWait(self, time):
        return [['wait',time]]
                    
class Enemy:
    
    def __init__(self, screen, pos, relPos, level, images, scaler):
        
        self.screen=screen
        self.pos=pos
        self.relPos = relPos
        self.level = level
        self.images = images
        self.scaler = scaler
        self.initWidth = 25.0
        self.initSpeed = 2.0
        self.status = 'available'
        self.direction = 'none'
        self.oldDirection = self.direction
        self.target = -1
        self.walkCounter = 0
        self.wait = 10 
        self.height = 0
        self.width = 0
        self.queue = []
        self.currentPic = 'front2'
        self.timer = -1
        self.wait = .1
        self.shootingTimer = -1
        self.hurtUser = False;
        self.hurtUserProb = .01
        
    def updatePosition(self,relPos,level):
        self.relPos = relPos
        self.level = level
        
    def updateQueue(self,directions):
        
        self.queue.extend(directions)
        
    def update(self):
        
        self.move()
        image = self.getImage()
        
        scaleFactor = self.scaler.scale(self.pos[1],self.initWidth)
        self.height = int(scaleFactor*image.get_size()[1])
        self.width = int(scaleFactor*image.get_size()[0])
        toDisplay = pygame.transform.scale(image,(self.width,self.height))
        self.screen.blit(toDisplay,(self.scaler.findX(self.pos[1],self.pos[0])-toDisplay.get_size()[0]/2,self.pos[1]-toDisplay.get_size()[1]))
        
    def getImage(self):
        
        if self.oldDirection!=self.direction:
            self.timer = time.time()
            if self.direction == 'forward':
                self.currentPic = 'front1'
            elif self.direction == 'left':
                self.currentPic = 'left1'
            elif self.direction == 'right':
                self.currentPic = 'right1'
            elif self.direction == 'shoot':
                self.currentPic = 'shoot1'
            else:
                self.currentPic = 'front2'
        elif time.time() - self.timer > self.wait:
            if self.currentPic == 'front1':
                self.currentPic = 'front3'
            elif self.currentPic == 'left1':
                self.currentPic = 'left3'
            elif self.currentPic =='right1':
                self.currentPic = 'right3'
            elif self.currentPic == 'front3':
                self.currentPic = 'front1'
            elif self.currentPic == 'left3':
                self.currentPic = 'left1'
            elif self.currentPic =='right3':
                self.currentPic = 'right1'
            elif self.currentPic =='shoot1':
                if random.random() < self.hurtUserProb:
                    self.hurtUser = True
                self.currentPic = 'shoot2'
            elif self.currentPic =='shoot2':
                self.currentPic = 'shoot1'
            self.timer = time.time()
            
        self.oldDirection = self.direction
            
        return self.images[self.currentPic]
    
    def move(self):
        
        if self.status != 'available':
            speed = .2*(self.initSpeed*self.scaler.scale(self.pos[1],self.initSpeed))**2
            if self.direction=='forward':
                self.pos = (self.pos[0],self.pos[1]+speed)
                if self.pos[1] > self.target:
                    self.pos = (self.pos[0],self.target)
                    self.status='available'
                    self.direction='none'
                    self.target=-1
            elif self.direction=='left':
                roadWidth = self.scaler.scale(self.pos[1],self.scaler.xRange1[1]-self.scaler.xRange1[0])*(self.scaler.xRange1[1]-self.scaler.xRange1[0])
                self.pos = (self.pos[0]-speed/roadWidth,self.pos[1])
                if self.pos[0] < self.target:
                    self.pos = (self.target,self.pos[1])
                    self.status='available'
                    self.direction='none'
                    self.target=-1
            elif self.direction=='right':
                roadWidth = self.scaler.scale(self.pos[1],self.scaler.xRange1[1]-self.scaler.xRange1[0])*(self.scaler.xRange1[1]-self.scaler.xRange1[0])
                self.pos = (self.pos[0]+speed/roadWidth,self.pos[1])
                if self.pos[0] > self.target:
                    self.pos = (self.target,self.pos[1])
                    self.status='available'
                    self.direction='none'
                    self.target=-1
            elif self.direction=='shoot':
                if time.time() - self.shootingTimer > self.target:
                    self.status='available'
                    self.direction='none'
                    self.target=-1
            elif self.direction=='wait':
                if time.time() - self.shootingTimer > self.target:
                    self.status='available'
                    self.direction='none'
                    self.target=-1
                
        if self.status=='available' and len(self.queue)>0:
            self.status='moving'
            self.direction=self.queue[0][0]
            if self.direction == 'shoot' or self.direction == 'wait':
                self.shootingTimer = time.time()
            self.target=self.queue[0][1]
            self.queue.remove(self.queue[0])
        
    def isHit(self,pos):
        minPoint = (self.scaler.findX(self.pos[1],self.pos[0])-self.width/2.0,self.pos[1]-self.height)
        if(pos[0]>minPoint[0] and pos[0]<minPoint[0]+self.width):
            if(pos[1]>minPoint[1] and pos[1]<minPoint[1]+self.height):
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
        
        self.doCalibrate = True
        
        self.shooting = False
        
        self.background = Background(self.screen)
        
        size = self.screen.get_size()
        self.scaler = Scaler((1/900.0*size[1],600/900.0*size[1]),(330/900.0*size[0],570/900.0*size[0]),(28/900.0*size[0],866/900.0*size[0]))
                
        self.cam = Camera(self.screen)

        self.gunChoice = [Gun(self.screen,self.cam, 10),Shotgun(self.screen,self.cam, 10)]
        self.gun = self.gunChoice[0]

        # self.menu = Menu(self.screen,'Enter the Game')

        self.pauses = False

        self.button = pygame.draw.rect(self.screen, (255,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/1.68,self.screen.get_size()[1]/2.5), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/10)))

        self.hud = HUD(self.screen)
        self.enMan = EnemyManager(self.screen,self.scaler,self.hud, 40, self.screen.get_size()[0]/20.0)
        self.track = pygame.mixer.music.load('gogo.wav') 
        self.shot = False
        pygame.mixer.music.play()

    def update(self):
         # Set the FPS of the game
        self.clock.tick(60)
        
        # Clear the screen
        self.screen.fill([100,200,100])
     
        if self.doCalibrate:
            i = 0
            while i<100:
                self.cam.calibrate()
                i +=1
            self.cam.endCalibration()
            self.doCalibrate = False

        
        for event in pygame.event.get():

            if event.type==QUIT:
                self.cam.endCam()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.cam.endCam()
                    exit()
                if event.key == K_SPACE:  

                    pos = (self.cam.x,self.cam.y)
                    if self.gun.isEmpty():
                        break
                    else:
                        self.gun.ammo -= 1
                        self.shooting = True
                        self.enMan.checkHit(pos)
                        i = 0                        
                        while i < self.gun.numShot:
                            newpos = (pos[0]+self.gun.hitRadius/(random.random() +1), pos[1] + self.gun.hitRadius/(random.random()+1))
                            self.enMan.checkHit(newpos)
                            i+=1
                        self.track = pygame.mixer.music.load('shot.wav') 
                        pygame.mixer.music.play()

                if event.key == K_p:
                    self.pauses = not self.pauses
                    self.gun.bulletShow = not self.gun.bulletShow

        self.cam.update()
        self.gun.update()
        if self.hud.score > 10:
            self.gun = self.gunChoice[1]
        if self.pauses == False:
            if self.hud.health>0:
                self.background.update()
                self.enMan.update()
                
                if self.cam.blue <10:
                    self.gun.reloaded()
                    try:
                        self.track = pygame.mixer.music.load('reloadFinal.wav')        
                        pygame.mixer.music.play()
                    except ValueError:
                        pass

                elif self.cam.green == 0:
                    pos = (self.cam.x,self.cam.y)
                    
                    if self.gun.isEmpty():
                        pass
                    elif not self.shot:
                        self.shot = True
                        self.gun.ammo -= 1
                        self.shooting = True
                        self.enMan.checkHit(pos)
                        i = 0                        
                        while i < self.gun.numShot:
                            newpos = (pos[0]+self.gun.hitRadius/(random.random() +1), pos[1] + self.gun.hitRadius/(random.random()+1))
                            self.enMan.checkHit(newpos)
                            i+=1
                        self.track = pygame.mixer.music.load('shot.wav') 
                        pygame.mixer.music.play()
                else:
                    self.shot = False
                        
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

        else:
            self.hud.pauseGame()
            
            if self.gun.x<self.screen.get_size()[0]-self.screen.get_size()[0]/1.68-(self.screen.get_size()[0]/5)/2 or self.gun.x >self.screen.get_size()[0]-self.screen.get_size()[0]/1.68+(self.screen.get_size()[0]/5)/2:
                self.pauses = True
            elif self.gun.y<self.screen.get_size()[1]-self.screen.get_size()[1]/1.68-(self.screen.get_size()[1]/10)/2 or self.gun.y >self.screen.get_size()[1]-self.screen.get_size()[1]/1.68+(self.screen.get_size()[1]/10)/2:
                self.pauses = True
            else:
                self.pauses = False
                self.gun.bulletShow = True

        pygame.display.flip()

if __name__ == '__main__':
  
    game = Main()
    while True:
        game.update()