#!/usr/bin/python
import pygame
from pygame.locals import *
import math
import numpy as np
from os import listdir
from os.path import isfile, join
import random
import numpy as np
import cv2

pygame.init() 

class Menu():
    def __init__(self, screen, items, backGroundColor=(0,200,0), font=None, fontSize=30, fontColor=(255, 255, 255)):

        self.screen = screen
        self.screenWidth = self.screen.get_rect().width
        self.screenHeight = self.screen.get_rect().height
        self.backGroundColor = backGroundColor
        self.items = items
        self.font = pygame.font.SysFont(font, fontSize)
        self.fontColor = fontColor

        self.clock = pygame.time.Clock()
 
        self.items = []
        for item in items:
            label = self.font.render(item, 1, fontColor)
 
            width = label.get_rect().width
            height = label.get_rect().height
            totalHeightTextBox = len(items) * height
            
            coordinates = ((self.screenWidth / 2) - (width / 2),(self.screenHeight / 2) - (totalHeightTextBox / 2))
 
            self.items.append([item, label, (width, height), coordinates])
 
    def run(self):
        mainloop = True
        while mainloop:
            self.clock.tick(50)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            self.screen.fill(self.backGroundColor)
 
            for name, label, (width, height), coordinates in self.items:
                self.screen.blit(label, coordinates)
 
            pygame.display.flip()
 
if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('Start', 'Settings','Quit')
 
    pygame.display.set_caption('Shooter Platform Game Menu')
    res = Menu(screen, menu_items)
    res.run()