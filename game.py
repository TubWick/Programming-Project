import pygame
from fighter import Fighter
from characterselection import Charselectionscreen
pygame.init()


#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption("Fighting game")

colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)
#define fighter variables
FIGHTER_SIZE = 200
#the scale for each sprite
FIGHTER_SCALE = 4

#manual offset so that the sprite is within the hitbox
MEDIUM_FIGHTER_OFFSET = [90,83]
HEAVY_FIGHTER_OFFSET = [90,80]

MEDIUM_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, MEDIUM_FIGHTER_OFFSET]
HEAVY_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, HEAVY_FIGHTER_OFFSET]
#create background image
bg_image= pygame.image.load("files/assets/background.png").convert_alpha()

#load spritesheet
#light_fighter_sheet = pygame.image.load("files/assets/Light Fighter Spritesheet.png").convert_alpha()
medium_fighter_sheet = pygame.image.load("files/assets/Normal Fighter Spritesheet.png").convert_alpha()
heavy_fighter_sheet = pygame.image.load("files/assets/Heavy Fighter Spritesheet.png").convert_alpha()
#number of steps for each animation
medium_animation_steps  = [4,6,2,3,3,1,5,3,1]
heavy_animation_steps =   [4,4,3,3,3,1,4,3,1]
#set framerate
clock = pygame.time.Clock()

def draw_bg():
    width = screen.get_width()
    height = screen.get_height()
    scaled_bg = pygame.transform.scale(bg_image, (width, height))
    screen.blit(scaled_bg, (0, 0))

#function for drawing healthbar
def draw_healthbar(health, x,y):
    health_ratio = health/100
    pygame.draw.rect(screen, (139,0,0), (x-3,y-3,406,36))
    pygame.draw.rect(screen, (139,0,0), (x,y,400,30))
    pygame.draw.rect(screen, (255,0,0), (x,y,400*health_ratio,30))
    
def draw_finisherbar(finisher_value, x, y):
    pygame.draw.rect(screen,(colour_dark), (x-3,y-3,206,26))
    pygame.draw.rect(screen,(26, 43, 68), (x,y,200,20))
    pygame.draw.rect(screen, (59, 130, 246), (x,y,0+finisher_value,20))



width = screen.get_width()
height = screen.get_height()


#instantiate fighters
fighter_1 = Fighter(200,350,"a","d","w","x","c","v",100,MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
fighter_2 = Fighter(700,350,"LEFT","RIGHT","UP","B","N","M",100,HEAVY_FIGHTER_DATA, heavy_fighter_sheet, heavy_animation_steps)



#game loop
run = True
while run:

    clock.tick(60)

    #draw background
    draw_bg()
    
    #show player health
    draw_healthbar(fighter_1.health,20,20)
    draw_healthbar(fighter_2.health,580,20)
   
    #draw player finisher
    draw_finisherbar(fighter_1.finisher_value,20,60)
    draw_finisherbar(fighter_2.finisher_value,780,60)

    #move fighters
    fighter_1.move(width,height,screen,fighter_2,fighter_1)
    fighter_2.move(width,height,screen,fighter_1,fighter_2)

    #frame handling
    fighter_1.frame_handler()
    fighter_2.frame_handler()

    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update dislay
    pygame.display.update()

pygame.quit()