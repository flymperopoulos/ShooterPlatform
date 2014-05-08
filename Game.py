# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 21:29:13 2014

@authors: 

Sidd Singal
James Jang
Filippos Lymperopoulos

Shooter Platform

You are under attack by the military, and you must shoot them to defend
youself. The enemies maneuver around walls and try to shoot back at you. 
Survive as long as you can. This game uses a physical replica gun to shoot
with in the game using openCV libraries.

"""

# Import all needed libraries
import pygame
from pygame.locals import *
import numpy as np
from os import listdir
from os.path import isfile, join
import random
import cv2
import time

'''
Camera

This class handles all of the interaction with the webcam by tracking 
different colors and their sizes
'''
class Camera:
    
    '''
    __init__
    
    Initialize the Camera class
        parameters:
            screen - the screen of the game
        returns: none
    '''
    def __init__(self, screen):
        
        # The pyGame screen
        self.screen = screen
        
        # Initialize the camera port
        self.cam = cv2.VideoCapture(0)
        
        # Initialize position of interest (where the gun is pointing)
        self.x=0
        self.y=0
        
        # Camera Blue and green values 
        self.blue = 0
        self.green = 0
        
        # Realgreen and realblue are for the calibration
        self.realgreen = 0
        self.realblue = 0
    
    '''
    calibrate
    
    Calibrate the camera to the static background by eliminating random 
    color noise
        parameters: none
        return: none
    '''
    def calibrate(self):
        """calibrate captures the extraneous background color"""
        # Capture frame-by-frame
        ret, frame = self.cam.read()

        # define range of blue color in HSV
        lower_green = np.uint8([40, 100, 100])
        upper_green = np.uint8([70, 255, 255])
        
        # define range of blue color in HSV
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])
        
        # change the BGR frame toe HSV (hue saturation value)       
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # inRange returns black white verison of the color bounds between the lower and upper 
        green = cv2.inRange(hsv, lower_green, upper_green)
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # add up the all of the background for each color
        self.realgreen += green
        self.realblue += blue
        
    '''
    endCalibration
    
    End the calibration and saves the background static image
    
    '''
    def endCalibration(self):
        self.realgreen[np.where(self.realgreen != 0)] = 255
        cv2.imwrite('initalgreen.png', self.realgreen)
        self.realgreen = cv2.imread('initalgreen.png', 0)
            
        self.realblue[np.where(self.realblue != 0)] = 255
        cv2.imwrite('initalblue.png', self.realblue)
        self.realblue = cv2.imread('initalgreen.png', 0)
        cv2.destroyAllWindows()
        
    '''
    update
    
    Updates the camera and sets the position and size of each color
        parameters: none
        returns: none
    '''    
    def update(self):
        # Capture frame-by-frame
        ret, frame = self.cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of blue color in HSV
        lower_blue = np.uint8([110, 100, 100])
        upper_blue = np.uint8([130,255,255])

        # define range of green color in HSV
        lower_green = np.uint8([40, 100, 100])
        upper_green = np.uint8([70, 255, 255])
        
        # inRange returns black white verison of the color bounds between the lower and upper         
        blue = cv2.inRange(hsv, lower_blue, upper_blue)
        green = cv2.inRange(hsv, lower_green, upper_green)
        
        # moments contain the position of the color mass         
        moment = cv2.moments(blue)

        # length of the number of pixels of green
        self.green = len(np.where(green != 0)[0])

        # finds the central x and y coordinates and scale it to the window
        if moment['m00'] != 0:
            x,y = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
            camWidth = self.cam.get(3)
            camHeight = self.cam.get(4)
            
            # set the x and y coordinates
            self.x = int((1.0*self.cam.get(3)-x)/camWidth*self.screen.get_size()[0])
            self.y = int((1.0*y)/camHeight*self.screen.get_size()[1])
            
            # length of the number of pixels of blue
            self.blue = len(np.where(blue == 255)[0])
            
    '''
    endCam
    
    Turns off the camera
        parameters: none
        returns: none
    '''
    def endCam(self):
        self.cam.release()
        cv2.destroyAllWindows()

'''
HUD

Represents the heads up dispay of the game, including health and score
'''
class HUD:
    
    '''
    __init__
    
    Initialize the HUD class
        parameters: 
            screen - the screen of the game
        returns: none
    '''
    def __init__(self,screen):
        
        # The pyGame screen
        self.screen = screen        
        
        # Initialize initial score and maximum health, and current health
        self.score = 0
        self.maxHealth = 100
        self.health = self.maxHealth
        
        # Initialize the font for any printed text
        self.font = pygame.font.SysFont("Comic Sans MS", self.screen.get_size()[1]/30)

    '''
    scoreUp
    
    Increase the score by 1
        parameters: none
        returns: none
    '''
    def scoreUp(self):
        
        # Increase the score by 1
        self.score+=1
    
    '''
    hurt
    
    The user is hurt when the enemy is able to make it all the way down
    to the bottom of the screen
        parameters: none
        returns: none
    '''        
    def hurt(self):
        
        # Decrease the health by 10
        self.health-=10
        
        # Display a red transparent rectangle signifying that 
        # the user is hurt
        hurtEnem = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  
        hurtEnem.set_alpha(100)                
        hurtEnem.fill((239,66,66))           
        self.screen.blit(hurtEnem, (0,0)) 
        
    '''
    shot
    
    The user is hurt when the enemy shoots successfully at the user
        parameters: none
        returns: none
    '''
    def shot(self):
        
        # Decrease the health by 1
        self.health-=1
        
        # Display a red transparent rectangle signifying that 
        # the user is hurt
        hurtEnem = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  
        hurtEnem.set_alpha(100)                
        hurtEnem.fill((239,66,66))           
        self.screen.blit(hurtEnem, (0,0)) 
        
    '''
    update
    
    Update all the figures on the screen
        parameters: none
        returns: none
    '''
    def update(self):
        
        # Display the health bar on the screen
        pygame.draw.rect(self.screen, (255,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/4.5,self.screen.get_size()[1]/25), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/70)))
        pygame.draw.rect(self.screen, (103,171,216), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/4.5,self.screen.get_size()[1]/24), ((self.screen.get_size()[0]/5)*1.0*self.health/self.maxHealth,self.screen.get_size()[1]/90)))        
        
        # Display the numerical health and score
        text1 = self.font.render("Score: " + str(self.score), 1, (10, 10, 10))
        text2 = self.font.render("Health: " + str(100/self.maxHealth*self.health) + '%', 1, (10, 10, 10))
        self.screen.blit(text1,(self.screen.get_size()[0]/12,self.screen.get_size()[1]/13))
        self.screen.blit(text2,(self.screen.get_size()[0]-self.screen.get_size()[0]/5.1,self.screen.get_size()[1]/17))
        
    '''
    endGame
    
    Displays the score at the end of the game
        parameters: none
        returns: none
    '''
    def endGame(self):
        
        # Set the text for the score to display
        text = self.font.render("Score: " + str(self.score), 1, (10, 10, 10))
        
        # Center and display the text        
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        textpos.centery = self.screen.get_rect().centery
        self.screen.blit(text, textpos)
        
    '''
    pauseGame
    
    A screen for when the game is paused
        parameters: none
        returns: none
    '''
    def pauseGame(self):
        
        # Set text indicating where the user should click to exit pause
        text = self.font.render("Continue",1, (10, 10, 10))
        
        # Display the text on the screen
        pygame.draw.rect(self.screen, (255,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/1.68,self.screen.get_size()[1]/2.5), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/10)))
        pygame.draw.rect(self.screen, (100,240,130), Rect((self.screen.get_size()[0]-self.screen.get_size()[0]/1.2,self.screen.get_size()[1]/2.5), (self.screen.get_size()[0]/5,self.screen.get_size()[1]/10)))        
        self.screen.blit(text,(self.screen.get_size()[0]/2.3,self.screen.get_size()[1]/2.34))
       
'''
Background

Represents the background for the game
'''
class Background:
    
    '''
    __init__
    
    Initialize the Background class
        parameters: none
        returns: none
    '''
    def __init__(self, screen):
        
        # The pyGame screen
        self.screen = screen
        
        # Load the background image from file
        self.bgImage = pygame.transform.scale(pygame.image.load('landscape.png'),self.screen.get_size())
        
    '''
    update
    
    Display the background on the screen
        parameters: none
        returns: none
    '''
    def update(self):
        
        # Add the background image to the screen
        self.screen.blit(self.bgImage,(0,0))
        
'''
Gun

Represents the gun and its current properties, and displays the crosshair
on the screen
'''
class Gun(object):
   
    '''
    __init__
    
    Initialize the Gun class
        parameters:
            screen - the screen of the game
            cam - the Camera input, to get its x and y values
            ammo - the maximum amount of ammo in the gun
        returns: none
    '''
    def __init__(self,screen,cam, ammo):
        
        # The pyGame screen
        self.screen = screen

        # The Camera of the game        
        self.cam = cam
        
        # Initiailize position of crosshair
        self.x = 0
        self.y = 0 
        
        # Load the image/size of the crosshair and bullet into the game
        self.crosshair = pygame.image.load('target.png')
        self.bullet = pygame.image.load('bullet.png').convert_alpha()
        self.gunSize = self.crosshair.get_size()
        
        # Initiailze the ammo and ammo to reload to 
        self.ammo = ammo
        self.rAmmo = ammo
        
        # The bullets should only be shown when the game is being played
        self.bulletShow = True
        
        # Set the font of the text
        self.font = pygame.font.SysFont("Comic Sans MS", self.screen.get_size()[1]/30)
        
        # Set the hit radius of the gun and the number of
        # bullets the gun shoots        
        self.hitRadius = self.screen.get_size()[1]/100
        self.numShot =1
        
        
    '''
    reloaded
    
    Reloads the gun
        parameters: none
        returns: none
    '''
    def reloaded(self):
        
        # Reset the ammo to the reload amount
        self.ammo = self.rAmmo

    '''
    isEmpty
    
    Checks if the gun is out of ammo
        parameters: none
        returns: True or False depending on if ammo has run out
    '''
    def isEmpty(self):
        
        # If the amount of ammo is 0, then return True, else return False
        if self.ammo == 0:
            return True
        return False
        
    '''
    update
    
    Update the Gun class, including crosshair position and bullets
        parameters: none
        returns: none
    '''
    def update(self):
       
        # If the game is being played, then show the bullets in the corner
        if self.bulletShow:
            
            # Show a bullet for every ammo the user's gun has
            for i in range(1,self.ammo+1):
                toShow = pygame.transform.scale(self.bullet, (int(0.3*(self.bullet.get_size()[0])), int(0.3*(self.bullet.get_size()[1]))))
                self.screen.blit(toShow,(self.screen.get_size()[0]/30*i,self.screen.get_size()[1]/35))
            
            # If there are no more bullets, indicate that the gun is empty
            if self.isEmpty():
                
                # Display the 'Gun is Empty' text where the bullets should be
                text3 = self.font.render("Gun is Empty", 1,(240, 10, 10))        
                self.screen.blit(text3,(self.screen.blit(text3,(self.screen.get_size()[0]/16,self.screen.get_size()[1]/25))))

        # Set the crosshair position to the position indicated by the camera
        self.x = self.cam.x
        self.y = self.cam.y
        
        # Display the crosshair on the screen
        self.screen.blit(self.crosshair,(self.x-self.gunSize[0]/2,self.y-self.gunSize[1]/2))       

'''
Shotgun

Shotgun that extends the Gun class, with different properties as the normal
Gun class
'''
class Shotgun(Gun):
    
    '''
    __init__
    
    Initialize the Shotgun class
        parameters:
            screen - the screen of the game
            cam - the Camera input, to get its x and y values
            ammo - the maximum amount of ammo in the gun
        returns: none
    '''
    def __init__(self,screen,cam, ammo):
        
        # Call init of the Gun superclass
        super(Shotgun, self).__init__(screen, cam, ammo)
        
        # Modify the hit radius, number of shots, and crosshair size
        self.hitRadius = self.screen.get_size()[1]/20
        self.numShot = 25
        self.crosshair = pygame.transform.scale2x(pygame.image.load('target.png'))

class Bomb(Gun):
    '''
    __init__
    
    Initialize the Bomb class
        parameters:
            screen - the screen of the game
            cam - the Camera input, to get its x and y values
            ammo - the maximum amount of ammo in the gun
        returns: none

    As with the Shotgun class, the Bomb class inherits from the Gun class. 
    '''
    def __init__(self,screen,cam, ammo):
        
        # Call init of the Gun superclass
        super(Bomb, self).__init__(screen, cam, ammo)
        
        # Modify the hit radius, number of shots, and crosshair size
        self.hitRadius = self.screen.get_size()[1]/20
        self.numShot = 25
        self.crosshair = pygame.transform.scale2x(pygame.image.load('bomb1.png'))
     
'''
Scalar

It is used to scale different objects to different sizes depending on
where the object is down the road. This helps make a 3-D effect in the game.
'''
class Scaler:
    
    '''
    __init__
    
    Initialize the Scalar class
        parameters:
            yRange - the values of two sample y values of the road
            xRange1 - the values of the road beginning and ending x value
                      corresponding to the first yRange value
            xRange2 - the values of the road beginning and ending x value
                      corresponding to the second yRange value
        returns: none
    '''
    def __init__(self, yRange, xRange1, xRange2):
        
        # Initializes the yRange, xRange1, and xRange2
        self.yRange = yRange
        self.xRange1 = xRange1
        self.xRange2 = xRange2
        
    '''
    scale
    
    Finds the scaling factor for a width of an object at the y=1 position
    of the road for a given y position on the road
        parameters:
            yVal - the y value corresponding to the road position to which
                   the width should be scaled to
            initWidth - the width of the object at y=1 of the road
        returns:
            The scaling factor of the object
    '''
    def scale(self,yVal,initWidth):
        
        # Find scaled width at the second yRange value
        wScaled=(self.xRange2[1]-self.xRange2[0])*initWidth/(self.xRange1[1]-self.xRange1[0])
        
        # Find the relative Y coordinate multiple in relation to the second
        # yRange value
        relY = yVal*1.0/(self.yRange[1]-self.yRange[0])
        
        # Find the width at the given y value and return a scaling factor
        newWidth = (wScaled-initWidth)*relY+initWidth
        return newWidth/initWidth
        
    '''
    findX
    
    Finds the exact x cooridnate given the y position on the road and the
    relative x position on the road
        parameters:
            yVal - y position on road for which x position needs to be found
            relX - relative x position on road at given y value
        returns:
            x position on screen corresponding to given y value and rel. x
    '''
    def findX(self,yVal,relX):
        
        # Find relative y distance as a scalar multiple of 2nd yRange value
        relDist = 1.0*(yVal-self.yRange[0])/(self.yRange[1]-self.yRange[0])
        
        # Find road width at given y value
        newRoadWidth = 1.0*((self.xRange2[1]-self.xRange2[0])-(self.xRange1[1]-self.xRange1[0]))*relDist+(self.xRange1[1]-self.xRange1[0])
        
        # Return absolute x position, after calculating offset from beginning
        # of road and x position relative to the beginning of the road
        xValOffset = newRoadWidth*relX
        startX = (self.xRange2[0]-self.xRange1[0])*relDist+self.xRange1[0]
        return startX + xValOffset
        
        
'''
Wall

Represents a wall that the enemies can hide behind
'''    
class Wall:
    
    '''
    __init__
    
    Initialize the Wall class
        parameters:
            screen - pyGame screen
            pos - bottom center position of the wall
            width - width of the wall
            height - height of the wall
            image - a picture of the wall
        returns: none
    '''
    def __init__(self, screen, pos, width, height, image):
        
        # The pyGame screen
        self.screen = screen
        
        # Position, width, and height of wall
        self.pos = pos
        self.height = height
        self.width = width
        
        # Load actual image of wall
        self.image = pygame.transform.scale(image, (int(self.width),int(self.height)))
        
    '''
    isHit
    
    Checks if wall has been hit by a bullet
    parameters:
        pos - position of bullet
    returns:
        True if wall is hit, and false otherwise
    '''    
    def isHit(self,pos):
        
        # Wall is not hit if the x position of pos is outside the wall boundaries
        if pos[0]<self.pos[0]-self.width/2 or pos[0]>self.pos[0]+self.width/2:
            return False
        
        # Wall is not hit if the y position of pos is outside the wall boundaries
        elif pos[1]<self.pos[1]-self.height or pos[1]>self.pos[1]:
            return False
            
        # Wall is hit if code reaches this far
        else:
            return True
        
    '''
    update
    
    Display the wall on the screen
        parameters: none
        returns: none
    '''
    def update(self):
        
        # Display the image of the wall on the screen and a black outline
        pygame.draw.rect(self.screen,(0,0,0),Rect((int(self.pos[0]-self.width/2.0)-2,int(self.pos[1]-self.height)-2),((int(self.width)+4,int(self.height)+4))))
        self.screen.blit(self.image,(int(self.pos[0]-self.width/2.0),int(self.pos[1]-self.height)))
    
'''
WallRow

Represents a row of walls on the road
'''
class WallRow:
    
    '''
    __init__
    
    Initializes the WallRow class
        parameters:
            screen - the game screen
            yPos - y position of the row of walls
            height - height of the walls in the class
            scalar - the scalar class to help scale walls
            edged - indicates if walls touch edges of road
            gapWidth - the sizes of gaps between the walls
            numGaps - the number of gaps
            last - indicates if this is the last wall row
            wallImage - image of the wall
        returns: none
    '''
    def __init__(self,screen,yPos,height,scaler,edged, gapWidth, numGaps, last, wallImage):
        
        # The pyGame screen
        self.screen = screen
        
        # y position and height of wall row
        self.yPos = yPos
        self.height=height
        
        # Scaler to help scale walls
        self.scaler=scaler
        
        # Determines of walls touch egdges
        self.edged = edged
        
        # Gap widths and number of gaps
        self.gapWidth = gapWidth
        self.numGaps = numGaps
        
        # Is this the last wall row?
        self.last = last
        
        # image of the wall
        self.wallImage = wallImage

        # List to store all the walls        
        self.walls = []        
        
        # Lists/variable to store x positions and y position of covers and
        # exits of the wall row
        self.xCovers = []
        self.xExits = []
        self.yCover = yPos - height*.2
        
        # If the wall row is edged, then the number of covers/exits is twice
        # the number of gaps
        if edged:
            self.positions = range(numGaps*2)
            
        # Otherwise it is twice one less the number of gaps
        else:
            self.positions = range((numGaps-1)*2)
            
        # Find the width of the road at the y position of the wall row
        roadWidth = scaler.scale(yPos,scaler.xRange1[1]-scaler.xRange1[0])*(scaler.xRange1[1]-scaler.xRange1[0])
        
        # Find the number of walls given if the wall row is edged and
        # the number of gaps
        walls = 0
        if edged:
            walls = numGaps + 1
        else:
            walls = numGaps - 1
            
        # Find the width of each wall in the wall row
        wallWidth = (roadWidth - numGaps*gapWidth)/walls
        
        # Find the x position at the beginning of the road at the given
        # y value of the road
        xInit = self.scaler.findX(self.yPos,0)
        
        # If the wall row is edged
        if edged:
            
            # For each wall
            for i in range(numGaps+1):
                
                # Find the x position of the wall and add it to the list of walls
                xPos = i*wallWidth+i*gapWidth+wallWidth/2+xInit
                self.walls.append(Wall(self.screen,(xPos,self.yPos),wallWidth, self.height, self.wallImage))
                
                # Add the x positions of all the covers and exits of the wall
                # row, depending on if the wall is on the ends or in the
                # middle
                if i==0:
                    self.xCovers.append((xPos+wallWidth/4.0-xInit)/roadWidth)
                    self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-xInit)/roadWidth)
                elif i==numGaps:
                    self.xCovers.append((xPos-wallWidth/4.0-xInit)/roadWidth)
                    self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-xInit)/roadWidth)
                else:
                    self.xCovers.append((xPos-wallWidth/4.0-xInit)/roadWidth)
                    self.xCovers.append((xPos+wallWidth/4.0-xInit)/roadWidth)
                    self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-xInit)/roadWidth)
                    self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-xInit)/roadWidth)
                    
        # But if the wall is not edged
        else:
            
            # For each wall
            for i in range(numGaps-1):
                
                # Find the x position of the wall and add it to the list of walls
                xPos = i*wallWidth+i*gapWidth+wallWidth/2+gapWidth+xInit
                self.walls.append(Wall(self.screen,(xPos,self.yPos),wallWidth, self.height, self.wallImage))
                
                # Add the x positions of the covers and exits
                self.xCovers.append((xPos-wallWidth/4.0-xInit)/roadWidth)
                self.xCovers.append((xPos+wallWidth/4.0-xInit)/roadWidth)
                self.xExits.append((xPos-wallWidth/2.0-gapWidth/4.0-xInit)/roadWidth)
                self.xExits.append((xPos+wallWidth/2.0+gapWidth/4.0-xInit)/roadWidth)
                
    '''
    isHit
    
    Checks to see if any of the walls in the wall row is hit
    
    parameters:
        pos - position of bullet
    returns:
        True if any walls are hit, and false otherwise
    '''
    def isHit(self,pos):
        
        # Check if any of the walls are hit
        for wall in self.walls:
            if wall.isHit(pos):
                return True
                
        # If none of the walls are hit, return False
        return False
        
    '''
    update
    
    Display all the walls in the wall row
    '''
    def update(self):
        
        # Display each wall in the wall row
        for wall in self.walls:
            wall.update()

'''
Enemy

Represents all the enemies in the game
'''
class Enemy:
    
    '''
    __init__
    
    Initializes the Enemy class
        parameters:
            screen - the game screen
            pos - the position of the enemy
            relPos - relative position of enemy in relation to wallRow 
                     cover index
            level - the level wallRow the enemy is at
            images - sprites for the enemies
            scalar - to help scale the enemy sizes
        returns: none
    '''
    def __init__(self, screen, pos, relPos, level, images, scaler):
        
        # The pyGame screen
        self.screen=screen

        # The initial position of the enemy. The y position of the enemy is 
        # stored as the pixel position on the screen, and the x position is 
        # stored as a value from [0,1], depending on how far along the enemy
        # is on the road
        self.pos=pos
        
        # Position of enemy in terms of cover index and wallRow index
        self.relPos = relPos
        self.level = level
        
        # Images to visually represent enemies
        self.images = images
        
        # Scaler to help scale the enemy sizes on the screen
        self.scaler = scaler
        
        # Initial width and speed of enemies
        self.initWidth = 25.0
        self.initSpeed = 2.0
        
        # Store the height and width of enemy so other classes can access it
        self.height = 0
        self.width = 0

        # Resetting the directions given to the enemy, and making him
        # available for instructions. This includes a queue of instructions,
        # current status of enemy, its direction, and its target
        self.queue = []
        self.status = 'available'
        self.direction = 'none'
        self.oldDirection = self.direction
        self.target = -1
        
        # Specifically to limit time enemy shoots for
        self.shootingTimer = -1
        
        # Variables to control changing of enemy pictures so they are
        # animated. Timer will store current time of program, wait stores
        # time between picture changes
        self.currentPic = 'front2'
        self.timer = -1
        self.wait = .1
        
        # To handle enemies succesfully shooting at user
        self.hurtUser = False;
        self.hurtUserProb = .01
        
    '''
    updatePosition
    
    Update the wallRow cover index and wallRow level index
        parameters:
            relPos - new wallRow cover index
            level - new wallRow level index
        returns: none
    '''    
    def updatePosition(self,relPos,level):
        
        # Set new relPos and level        
        self.relPos = relPos
        self.level = level
        
    '''
    updateQueue
    
    Allows other classes to update the queue of the enemy so it knows what
    to do
        parameters:
            directions - list of instructions for enemy
        returns: none
    '''
    def updateQueue(self,directions):
        
        # Add the given directions to the enemy's queue
        self.queue.extend(directions)
        
    '''
    getImage
    
    Finds the correct image of the enemy to display on the screen
        parameters: none
        returns:
            An image representing the enemy's state to display on the screen
    '''
    def getImage(self):
        
        # If the direction has changed
        if self.oldDirection!=self.direction:
            
            # Reset the timer
            self.timer = time.time()
            
            # Set the default picture based on the new direction of the enemy
            if self.direction == 'forward':
                self.currentPic = 'front1'
            elif self.direction == 'left':
                self.currentPic = 'left1'
            elif self.direction == 'right':
                self.currentPic = 'right1'
            elif self.direction == 'shoot':
                self.currentPic = 'shoot1'
            
            # If the enemy is not given a direction, then default to forward
            # facing image
            else:
                self.currentPic = 'front2'
                
        # If the direction has stayed the same, but too much time has passed
        # on a single image being displayed on the screen
        elif time.time() - self.timer > self.wait:
            
            # Switch between walking forward images
            if self.currentPic == 'front1':
                self.currentPic = 'front3'
            elif self.currentPic == 'front3':
                self.currentPic = 'front1'
                
            # Switch between walking left images
            elif self.currentPic == 'left1':
                self.currentPic = 'left3'
            elif self.currentPic == 'left3':
                self.currentPic = 'left1'
                
            # Switch between walking right images
            elif self.currentPic =='right1':
                self.currentPic = 'right3'
            elif self.currentPic =='right3':
                self.currentPic = 'right1'
                
            # Switch between shooting images
            elif self.currentPic =='shoot1':
                
                # Randomly determine if enemy has succesfully shot user
                if random.random() < self.hurtUserProb:
                    self.hurtUser = True
                self.currentPic = 'shoot2'
            elif self.currentPic =='shoot2':
                self.currentPic = 'shoot1'
                
            # Reset the timer
            self.timer = time.time()
            
        # Set oldDirection variable to compare for next iteration
        self.oldDirection = self.direction
        
        # Return appropriate image
        return self.images[self.currentPic]
    
    '''
    move
    
    Moves the enemy depending on the instructions it has in its queue
        parameters: none
        returns: none
    '''
    def move(self):
        
        # If the enemy is not avaiable for new instructions
        if self.status != 'available':
            
            # Find the speed of the enemy based on its y position
            speed = .2*(self.initSpeed*self.scaler.scale(self.pos[1],self.initSpeed))**2
            
            # If the enemy's current direction is forward
            if self.direction=='forward':
                
                # Update the position of the enemy so he walks forward
                self.pos = (self.pos[0],self.pos[1]+speed)
                
                # If the enemy has reached its target, reset his status and 
                # make him available for new instructions
                if self.pos[1] > self.target:
                    self.pos = (self.pos[0],self.target)
                    self.status='available'
                    self.direction='none'
                    self.target=-1
            
            # If the enemy's current direction is left
            elif self.direction=='left':
                
                # Find the width of the road so that speed can properly be
                # scaled. Then update the enemy position to make him walk left
                roadWidth = self.scaler.scale(self.pos[1],self.scaler.xRange1[1]-self.scaler.xRange1[0])*(self.scaler.xRange1[1]-self.scaler.xRange1[0])
                self.pos = (self.pos[0]-speed/roadWidth,self.pos[1])
                
                # If the enemy has reached its target, reset his status and 
                # make him available for new instructions
                if self.pos[0] < self.target:
                    self.pos = (self.target,self.pos[1])
                    self.status='available'
                    self.direction='none'
                    self.target=-1
                    
            # If the enemy's current direction is right
            elif self.direction=='right':
                
                # Find the width of the road so that speed can properly be
                # scaled. Then update the enemy position to make him walk right
                roadWidth = self.scaler.scale(self.pos[1],self.scaler.xRange1[1]-self.scaler.xRange1[0])*(self.scaler.xRange1[1]-self.scaler.xRange1[0])
                self.pos = (self.pos[0]+speed/roadWidth,self.pos[1])
                
                # If the enemy has reached its target, reset his status and 
                # make him available for new instructions
                if self.pos[0] > self.target:
                    self.pos = (self.target,self.pos[1])
                    self.status='available'
                    self.direction='none'
                    self.target=-1
                    
            # If the enemy is instructed to shoot
            elif self.direction=='shoot':
                
                # Reset status if enemy has been shooting for long enough
                if time.time() - self.shootingTimer > self.target:
                    self.status='available'
                    self.direction='none'
                    self.target=-1
                    
            # If enemy is instructed to wait
            elif self.direction=='wait':
                
                # Reset status if enemy has been waiting for long enough
                if time.time() - self.shootingTimer > self.target:
                    self.status='available'
                    self.direction='none'
                    self.target=-1
        
        # If the enemy is avaialble for more instructions, and there are
        # instructions still in the queue
        if self.status=='available' and len(self.queue)>0:
            
            # Set the status of the enemy to not available (or moving)
            self.status='moving'
            
            # Set the new direction of the enemy
            self.direction=self.queue[0][0]
            
            # If the enemy has to shoot or wait, then start a timer
            if self.direction == 'shoot' or self.direction == 'wait':
                self.shootingTimer = time.time()
                
            # Store the target corresponding to the direction:
                # If direction is forward, then target is y position
                # If direction is left/right, then target is relative x position
            self.target=self.queue[0][1]
            
            # Remove instruction from the queue
            self.queue.remove(self.queue[0])
        
    '''
    isHit
    
    Determines if enemy has been hit by bullet
        parameters:
            pos - position of the bullet
        returns:
            True if enemy has been hit by bullet and False otherwise
    '''
    def isHit(self,pos):
        
        # Find the top left corner of the enemy
        minPoint = (self.scaler.findX(self.pos[1],self.pos[0])-self.width/2.0,self.pos[1]-self.height)
        
        # If the x position and y position lie within the boundaries of the
        # enemy then return True
        if(pos[0]>minPoint[0] and pos[0]<minPoint[0]+self.width):
            if(pos[1]>minPoint[1] and pos[1]<minPoint[1]+self.height):
                return True
                
        # Otherwise return False
        return False
        
    '''
    update
    
    Updates the position and display of the enemy
        parameters: none
        returns: none
    '''
    def update(self):
        
        # Change the position of the enemy
        self.move()
        
        # Find the right picture to use for the enemy
        image = self.getImage()
        
        # Resize the image depending on his y position
        scaleFactor = self.scaler.scale(self.pos[1],self.initWidth)
        self.height = int(scaleFactor*image.get_size()[1])
        self.width = int(scaleFactor*image.get_size()[0])
        toDisplay = pygame.transform.scale(image,(self.width,self.height))
        
        # Display the enemy on the screen
        self.screen.blit(toDisplay,(self.scaler.findX(self.pos[1],self.pos[0])-toDisplay.get_size()[0]/2,self.pos[1]-toDisplay.get_size()[1]))

            
'''
EnemyManager

This class handles all of the enemies and walls of the game
'''
class EnemyManager:
    
    '''
    __init__
    
    Initialize the EnemyManager class
        parameters: 
            screen - the screen of the game
            scaler - to help scale image sizes
            hud - heads up display of the game
            initWallHeight - the initial height of the wall
            initGapWidth - the initial width of the gaps between the walls
        returns: none
    '''    
    def __init__(self,screen,scaler,hud, initWallHeight, initGapWidth):
        
        # The pyGame screen
        self.screen = screen
        
        # Scaler for the class
        self.scaler = scaler
        
        # The heads up display of the game
        self.hud = hud
        
        # Initial height of the wall and initial width of gaps between walls
        self.initWallHeight = initWallHeight
        self.initGapWidth = initGapWidth

        # Load wall image        
        self.wallImage = pygame.image.load('wall.png')
        
        # Initialize empty arrays for enemies and creates array of wall rows
        self.enemies = []
        self.wallRows = []
        self.createWalls(5,.1,.9)
        
        # The probability that a new enemy appears in a given frame
        self.newEnemyProb = .01
        
        # Load the images of the enemy into the game
        self.enemyImages = {}
        enemyFiles = [ f for f in listdir('SoldierSprite/') if isfile(join('SoldierSprite/',f)) ]
        for f in enemyFiles:
            image = pygame.image.load('SoldierSprite/'+f)
            resized = pygame.transform.scale(image,(25,int(25.0/image.get_size()[0]*image.get_size()[1])))
            self.enemyImages[f[0:-4]]=resized
            
    '''
    checkHit
    
    Checks to see if enemy has been hit
        parameters:
            pos - position of bullet
        returns:
            True if enemy has been hit and False otherwise
    '''
    def checkHit(self,pos):
        
        # Sort the array of enemies by how close they are to the front
        self.enemies = sorted(self.enemies, key=lambda enemy: enemy.pos[1])
        
        # If the bullet was aimed toward a wall, make sure only enemies 
        # in front of the closest wall hit are considered
        minY = 0;
        for wallRow in self.wallRows:
            if wallRow.isHit(pos):
                minY = wallRow.yPos
        
        # Only check if enemies are hit only if they are in front of the 
        # closest wall hit
        for enemy in self.enemies[::-1]:
            if enemy.isHit(pos) and enemy.pos[1]>minY:
                self.enemies.remove(enemy)
                self.hud.scoreUp()
                break
            
    '''
    createWalls
    
    Create the walls in the game
        parameters:
            rows - the number of rows of walls
            minRelY - relative Y position of where the first row of walls 
                      should be
            maxRelY - relative Y position of wher ethe last row of walls
                      should be
        returns:
            none
    '''
    def createWalls(self, rows, minRelY, maxRelY):
        
        # Assume the first wallRow will not be edged with 3 gaps
        edged = False
        gaps = 3
        
        # Temporary variable to help determine amount of walls needed
        gapTemp = 0
        
        # For each row we want to create walls of
        for i in range(rows):
            
            # Scale the walls position so the distance between them is equal
            yTemp = (i*1.0/rows)**1.5
            yRange = maxRelY-minRelY
            yPos = (yTemp*yRange+minRelY)*self.screen.get_size()[1]
            
            # Find the pixel width of the gaps and the height of the walls
            gapWidth = self.scaler.scale(yPos,self.initGapWidth)*self.initGapWidth
            height = self.scaler.scale(yPos,self.initWallHeight)*self.initWallHeight
            
            # Add a new walLRow with the calculated arguments
            self.wallRows.append(WallRow(self.screen,yPos,height,self.scaler,edged,gapWidth,gaps-gapTemp,False,self.wallImage))
            
            # The next row will have the following properties
            edged = not edged
            gapTemp = 1-gapTemp
            
        # Indicate the last wall of rows to be the last
        self.wallRows[-1].last=True
                
    '''
    getPath
    
    Find a path for the enemies to move from one wall level to the next
        parameters:
            wallRowOld - The current wall row the enemy is on
            wallRowOldPos - the cover index on the current wall row the enemy
                            is on
            wallRowNew - the next wall row the enemy is to move on to
            wallRowNewPos - the cover index for enemy to move to on the next
                            row of walls
        returns: none
    '''
    def getPath(self, wallRowOld, wallRowOldPos, wallRowNew, wallRowNewPos):
        
        # Initialize an empty array of directions
        directions = []

        # The enemy will first move left or right to an exit of their wall
        # row depending on if the wall row is edged and which cover in the 
        # wall row the enemy is on
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
                
        # If the last wall row has been reached
        if wallRowOld.last:
            
            # Send the enemy forward off the screen
            directions.append(['forward',self.screen.get_size()[1]+100])
            
        # Otherwise
        else:
            
            # Send the enemy forward to the y position of the next wall row
            directions.append(['forward',wallRowNew.yCover])
            
            # Send the enemy left or right depending on where their new
            # cover is relative to them
            lastDir = 'left'
            if wallRowOld.xExits[wallRowOldPos] < wallRowNew.xCovers[wallRowNewPos]:
                lastDir = 'right'
            directions.append([lastDir,wallRowNew.xCovers[wallRowNewPos]])
        
        # Return the updated list of directions for the enemy
        return directions
        
    '''
    sendShoot
    
    Give the enemy directions to shoot at the player
        parameters:
            wallRowOld - the current wall row the enemy is at
            walRowOldPos - the cover index of the enemy
            time - the amount of the seconds the enemy should shoot for
    '''
    def sendShoot(self, wallRowOld, wallRowOldPos, time):
        
        # Initialize the directions to send to the enemy
        directions = []
        
        # The enemy will first move left or right to an exit of their wall
        # row depending on if the wall row is edged and which cover in the 
        # wall row the enemy is on
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
                
        # Instruct the enemy to shoot
        directions.append(['shoot',time])
        
        # Send the enemy back to his cover
        if directions[0][0] == 'left':
            directions.append(['right',wallRowOld.xCovers[wallRowOldPos]])
        else:
            directions.append(['left',wallRowOld.xCovers[wallRowOldPos]])
            
        # Give the enemy his instructions    
        return directions
        
    '''
    makeWait
    
    Make the enemy wait behind his cover
        parameters:
            time - the amount of time the enemy should wait for
        returns: none
    '''
    def makeWait(self, time):
        
        # Give the enemy the instructions to wait
        return [['wait',time]]
        
    '''
    update
    
    Update all the walls and enemies properties and images
        parameters: none
        returns: none
    '''
    def update(self):
        
        # Randomly decide if a new enemy should be placed on the screen
        if random.random()<=self.newEnemyProb:
            
            # Choose a random cover index
            index = random.randint(0,len(self.wallRows[0].xCovers)-1)
            pos = self.wallRows[0].xCovers[index]
            
            # Create a new enemy and send him the instruction to move forward
            # to his first cover
            newEnemy = Enemy(self.screen,(pos,1),index,0,self.enemyImages,self.scaler)
            newEnemy.updateQueue([['forward',self.wallRows[0].yCover]])
            self.enemies.insert(0,newEnemy)
            
            # Increase the probability that a new enemy will appear
            self.newEnemyProb+=.001
        
        # For each enemy that is alive
        for enemy in self.enemies:
            
            # If they are available to do a task
            if enemy.status =='available':
                
                # Randomly decide if they should shoot at the player, wait
                # behind their cover, or advance to the next wall row
                shootProb = .2
                waitProb = .3
                advanceProb = .5
                choice = random.random()
                
                # Shoot the player
                if choice < shootProb:
                    enemy.updateQueue(self.sendShoot(self.wallRows[enemy.level], enemy.relPos, 3.0))
                    
                # Wait behind cover
                elif choice < shootProb + waitProb:
                    enemy.updateQueue(self.makeWait(3.0))
                    
                # Advance to the next row
                elif choice < shootProb + waitProb + advanceProb:
                    
                    # ...if they are not in the last wall row
                    if not self.wallRows[enemy.level].last:
                        index = random.randint(0,len(self.wallRows[enemy.level+1].xCovers)-1)
                        pos = self.wallRows[enemy.level+1].xCovers[index]
                        enemy.updateQueue(self.getPath(self.wallRows[enemy.level],enemy.relPos,self.wallRows[enemy.level+1],index))
                        enemy.updatePosition(index,enemy.level+1)         
                    
                    # But if they are, then send them off the screen
                    else:
                        enemy.updateQueue(self.getPath(self.wallRows[enemy.level],enemy.relPos,None,None))
                    
        # For each enemy
        for enemy in self.enemies:
            
            # Check if the enemy has successfully shot the user and update
            # the HUD accordingly
            if enemy.hurtUser:
                enemy.hurtUser = False
                self.hud.shot()
                
            # Check if the enemy has successfully reached the bottom of the
            # screen and remove them if they have (and hurt the user)
            if enemy.pos[1]>self.screen.get_size()[0]:
                self.enemies.remove(enemy)
                self.hud.hurt()
                
        # Sort the array of enemies by their y position
        self.enemies = sorted(self.enemies, key=lambda enemy: enemy.pos[1])
                
        # Display all of the wall rows and enemies, starting from the back
        # of the road to the beginning. To do this, first find the total
        # number of wall roads and enemies and start the counters at 0
        entities = len(self.wallRows)+len(self.enemies)
        wrCounter = 0
        enemyCounter = 0
        
        # While not all enemies and wall rows have been shown
        while enemyCounter + wrCounter < entities:
            
            # If all the enemies have already been shown, show the rest of
            # the walls
            if enemyCounter == len(self.enemies):
                for i in range(wrCounter,len(self.wallRows)):
                    self.wallRows[i].update()
                wrCounter=len(self.wallRows)
                    
            # If all the wall rows have already been shown, show the rest of
            # the enemies
            elif wrCounter == len(self.wallRows):
                for i in range(enemyCounter,len(self.enemies)):
                    self.enemies[i].update()
                enemyCounter=len(self.enemies)
                    
            # But otherwise...
            else:
                
                # Find the y position of the next wall row and next enemy
                # to be displayed
                wallY = self.wallRows[wrCounter].yPos
                enemyY = self.enemies[enemyCounter].pos[1]
                
                # Display whichever is closer to the back of the road first:
                # the road or the wall
                if enemyY>wallY:
                    self.wallRows[wrCounter].update()
                    wrCounter+=1
                else:
                    self.enemies[enemyCounter].update()
                    enemyCounter+=1
                    
'''
Main

Main function for the game. 
'''
class Main:
    
    '''
    __init__
    
    Initialize the main class. Main class will contain all of the classes created in this game
        returns: none
    '''
    def __init__(self):
        
        # Initialize PyGame stuff
        pygame.init()
        infoObject = pygame.display.Info()
        
        # Finds the height and width of the screen to make all the position relative 
        screenWidth,screenHeight = infoObject.current_w, infoObject.current_h
        height=int(screenHeight)
        width=int(height)
        
        # Initializes the screen
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Shooter Platform')
        self.clock=pygame.time.Clock()
        
        # boolean for calibration to only do it once when the game starts        
        self.doCalibrate = True
        
        # boolean for pausing the game
        self.pauses = False
        
        self.shot = False        
        
        # Initializes the background
        self.background = Background(self.screen)
        
        size = self.screen.get_size()
        
        # Initializes the scalar
        self.scaler = Scaler((1/900.0*size[1],600/900.0*size[1]),(330/900.0*size[0],570/900.0*size[0]),(28/900.0*size[0],866/900.0*size[0]))

        # Initializes the camera                
        self.cam = Camera(self.screen)
        
        # Initializes the choices of the guns for upgrade
        self.gunChoice = [Gun(self.screen,self.cam, 10),Shotgun(self.screen,self.cam, 10)]
        self.gunChoice2 = [Gun(self.screen,self.cam, 10),Bomb(self.screen,self.cam, 10)]

        # Initializes the screen        
        self.gun = self.gunChoice[0]
        self.gun = self.gunChoice2[0]

        # self.menu = Menu(self.screen,'Enter the Game')
        
        # Initializes the HUD        
        self.hud = HUD(self.screen)
        
        # Initializes the EnemyManager
        self.enMan = EnemyManager(self.screen,self.scaler,self.hud, 40, self.screen.get_size()[0]/20.0)
        
        # Soundtrack to mark the start of the game
        self.track = pygame.mixer.music.load('gogo.wav') 
        
        pygame.mixer.music.play()

    '''
    update
    
    updates the whole game
    '''
    def update(self):
         # Set the FPS of the game
        self.clock.tick(60)
        
        # Clear the screen
        self.screen.fill([100,200,100])
        
        # Calibrate the screen
        if self.doCalibrate:
            
            # Calibrate for around 3 seconds            
            i = 0
            while i<100:
                self.cam.calibrate()
                i +=1
            self.cam.endCalibration()
            self.doCalibrate = False

        # For each user event the pygame has in its queue
        for event in pygame.event.get():

            # Quit if the user wants to quit
            if event.type==QUIT:
                self.cam.endCam()
                exit()
            
            # If a key has been pressed...
            if event.type == KEYDOWN:
                
                # If the escape key is pressed, quit the game
                if event.key == K_ESCAPE:
                    self.cam.endCam()
                    exit()
                
                # Keyboard key to shoot
                if event.key == K_SPACE: 
                    
                    # position of the gun
                    pos = (self.cam.x,self.cam.y)
                    
                    # check if the gun is empty
                    if self.gun.isEmpty():
                        break
                    else:
                        self.gun.ammo -= 1
                        self.shooting = True
                        
                        # Check to see if the enemy is hit and remove
                        self.enMan.checkHit(pos)
                        i = 0                        
                        
                        # Upgrades for the gun to make it shoot multiple times
                        while i < self.gun.numShot:
                            newpos = (pos[0]+self.gun.hitRadius/(random.random() +1), pos[1] + self.gun.hitRadius/(random.random()+1))
                            self.enMan.checkHit(newpos)
                            i+=1
                            
                        # plays a shooting sound
                        self.track = pygame.mixer.music.load('shot.wav') 
                        pygame.mixer.music.play()
                
                # Pause key
                if event.key == K_p:
                    self.pauses = not self.pauses
                    self.gun.bulletShow = not self.gun.bulletShow
        
        # update the gun and cam to track the cursor
        self.cam.update()
        self.gun.update()
    
        # upgrade the gun as the score goes up to shotgun    
        if self.hud.score > 3:
            self.gun = self.gunChoice[1]

        # upgrade gun option after 5 kills to a bomb
        if 4 <self.hud.score <6:
            self.gun = self.gunChoice2[1]

        # Pausing the game
        if self.pauses == False:
            if self.hud.health>0:
                self.background.update()
                self.enMan.update()
                
                # tracks the blue and if the blue disappears from the screen then reload the gun
                if self.cam.blue <10:
                    self.gun.reloaded()
                    try:
                        # reloading sound
                        self.track = pygame.mixer.music.load('reloadFinal.wav')        
                        pygame.mixer.music.play()
                    except ValueError:
                        pass
                
                # if the green disappears shoot
                elif self.cam.green == 0:
                    pos = (self.cam.x,self.cam.y)
                    
                    if self.gun.isEmpty():
                        pass
                    elif not self.shot:
                        
                        # shot boolean to a shoot only once
                        self.shot = True
                        self.gun.ammo -= 1
                        self.enMan.checkHit(pos)
                        
                        # shoot multiple times for gun upgrades depending on the gun's paramters
                        i = 0                        
                        while i < self.gun.numShot:
                            newpos = (pos[0]+self.gun.hitRadius/(random.random() +1), pos[1] + self.gun.hitRadius/(random.random()+1))
                            self.enMan.checkHit(newpos)
                            i+=1
                        self.track = pygame.mixer.music.load('shot.wav') 
                        
                        # flash the screen when the gun is shot 
                        s = pygame.Surface((self.screen.get_size()[0],self.screen.get_size()[1]))  # the size of your rect
                        s.set_alpha(128)                # alpha level
                        s.fill((255,255,255))           # this fills the entire surface
                        self.screen.blit(s, (0,0)) 
                        pygame.mixer.music.play()
                else:
                    self.shot = False

                self.hud.update()
                self.gun.update()
                
            # end game when the health = 0
            else:
                self.hud.endGame()
        
        # Pause the game
        else:
            self.hud.pauseGame()
            
            # Continue the game when the cursor is inside the continue box
            if self.gun.x<self.screen.get_size()[0]-self.screen.get_size()[0]/1.68-(self.screen.get_size()[0]/5)/2 or self.gun.x >self.screen.get_size()[0]-self.screen.get_size()[0]/1.68+(self.screen.get_size()[0]/5)/2:
                self.pauses = True
            elif self.gun.y<self.screen.get_size()[1]-self.screen.get_size()[1]/1.68-(self.screen.get_size()[1]/10)/2 or self.gun.y >self.screen.get_size()[1]-self.screen.get_size()[1]/1.68+(self.screen.get_size()[1]/10)/2:
                self.pauses = True
            else:
                self.pauses = False
                self.gun.bulletShow = True
        
        # display
        pygame.display.flip()
             
'''
Main function
'''
if __name__ == '__main__':
    
    # Start the game and run it indefinitely
    game = Main()
    while True:
        game.update()