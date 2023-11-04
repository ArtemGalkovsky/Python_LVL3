import pygame
import random

def draw_food(screen,color,x,y,radius):
    '''This function draws/creates the food sprite, The screen variable tells the food what screen to be drawn to. the color variable sets the color the radius variable sets how large of a circle the food will be.'''
    pygame.draw.circle(screen,green,(x,y),radius)

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
white = (255, 255, 255)
green = (0, 255, 0)
running = True

# main program loop
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((white))

    # Draw the food
    draw_food(screen,green,random.randint(0,width),random.randint(0,height),20)

    # Flip the display
    pygame.display.flip()
