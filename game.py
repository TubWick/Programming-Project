import pygame
from fighter import Fighter
pygame.init()


#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption = ("Fighting game")


#define fighter variablles
FIGHTER_SIZE = 200
FIGHTER_SCALE = 3
FIGHTER_OFFSET = [90,66]
FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE,FIGHTER_OFFSET]

#create background image
bg_image= pygame.image.load("files/assets/background.png").convert_alpha()

#load spritesheet
fighter_sheet = pygame.image.load("files/assets/Normal Fighter Spritesheet.png").convert_alpha()

#number of steps for each animation
FIGHTER_ANIMATION_STEPS  = [6,3,6,5,4,5,6,4]

#set framerate
clock = pygame.time.Clock()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (width,height))
    screen.blit(scaled_bg, (0,0))

#function for drawing healthbar
def draw_healthbar(health, x,y):
    health_ratio = health/100
    pygame.draw.rect(screen, (139,0,0), (x,y,400,30))
    pygame.draw.rect(screen, (255,0,0), (x,y,400*health_ratio,30))


width = screen.get_width()
height = screen.get_height()


#instantiate fighters
fighter_1 = Fighter(200,350,"a","d","w","x","c","v",100, FIGHTER_DATA, fighter_sheet, FIGHTER_ANIMATION_STEPS)
fighter_2 = Fighter(700,350,"LEFT","RIGHT","UP","B","N","M",100,FIGHTER_DATA, fighter_sheet, FIGHTER_ANIMATION_STEPS)



#game loop
run = True
while run:

    clock.tick(60)

    #draw background
    draw_bg()
    #show player health
    draw_healthbar(fighter_1.health,20,20)
    draw_healthbar(fighter_2.health,580,20)

    #move fighters
    fighter_1.move(width,height,screen,fighter_2)
    fighter_2.move(width,height,screen,fighter_1)

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
