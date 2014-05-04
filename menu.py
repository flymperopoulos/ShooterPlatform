#!/usr/bin/python
import pygame

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
        for index, item in enumerate(items):
            label = self.font.render(item, 1, fontColor)
 
            width = label.get_rect().width
            height = label.get_rect().height
            totalHeightTextBox = len(items) * height
            
            coordinates = ((self.screenWidth / 2) - (width / 2),(self.screenHeight / 2) - (totalHeightTextBox / 2) + (index * 1.5*height))
 
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

class TargetMove():

    def __init__(self,screen,target,targetSize):
        self.screen = screen
        self.taret = pygame.image.load('target.png')
        self.targetSize = self.target.get_size()

    def isSelected(self,pos):
        pass

    def update(self):
        self.x = self.cam.x
        self.y = self.cam.y
        self.screen.blit(self.crosshair,(self.x-self.gunSize[0]/2,self.y-self.gunSize[1]/2))

        for event in pygame.event.get():
            if event.key == K_SPACE:
        
                pos = (self.cam.x,self.cam.y)
                self.gun.ammo -= 1
                self.enMan.checkHit(pos)
                self.track = pygame.mixer.music.load('shot.wav') 
                pygame.mixer.music.play() 
 
if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('Start', 'Settings','Exit')
 
    pygame.display.set_caption('Shooter Platform Game Menu')
    res = Menu(screen, menu_items)
    res.run()