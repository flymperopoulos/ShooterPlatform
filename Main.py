import pygame

background_colour = (255,255,255)
(width, height) = (300, 200)

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Shooter Platform')

screen.fill(background_colour)

pygame.display.flip()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
    	False