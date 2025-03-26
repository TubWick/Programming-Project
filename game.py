import pygame
from fighter import Fighter
from characterselection import Charselectionscreen
pygame.init()

class Timer:
    def __init__(self):
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False 
        self.start_time = 0
    
    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            time_surf= smallfont.render(str((pygame.time.get_ticks() - (match_timer.start_time)) // 1000), True, (255,255,255)).convert_alpha()
            time_surf_outline= smallfont.render(str((pygame.time.get_ticks() - (match_timer.start_time)) // 1000), True, (0,0,0)).convert_alpha()
            screen.blit(time_surf_outline,(width//2 - 7, height//2 - 297))
            screen.blit(time_surf,(width//2 - 10, height//2 - 300))

match_timer = Timer()
match_timer.activate()


#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption("Fighting game")

smallfont = pygame.font.Font('files/mini_pixel-7.ttf',75)
gameoverfont = pygame.font.Font('files/mini_pixel-7.ttf',150)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)
#define fighter variables
FIGHTER_SIZE = 200
#the scale for each sprite
FIGHTER_SCALE = 4

#manual offset so that the sprite is within the hitbox
LIGHT_FIGHTER_OFFSET = [90,83]
MEDIUM_FIGHTER_OFFSET = [90,83]
HEAVY_FIGHTER_OFFSET = [80,80]

MEDIUM_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, MEDIUM_FIGHTER_OFFSET]
HEAVY_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, HEAVY_FIGHTER_OFFSET]
LIGHT_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, LIGHT_FIGHTER_OFFSET]
#create background image
bg_image= pygame.image.load("files/assets/background.png").convert_alpha()

#load spritesheet
light_fighter_sheet = pygame.image.load("files/assets/Light Fighter Spritesheet.png").convert_alpha()
medium_fighter_sheet = pygame.image.load("files/assets/Normal Fighter Spritesheet.png").convert_alpha()
heavy_fighter_sheet = pygame.image.load("files/assets/Heavy Fighter Spritesheet.png").convert_alpha()
#number of steps for each animation
light_animation_steps = [4,5,2,2,3,1,5,3,1]
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

def end_match(health,x,y):
    if health <= 0:
        current_time = pygame.time.get_ticks()
        flash_duration = 500
        if current_time // flash_duration % 2 == 0:      
            end_text_body = gameoverfont.render("K.O", True, ((255,10,20))).convert_alpha()
            end_text_outline = gameoverfont.render("K.O", True, (0,0,0)).convert_alpha()
            end_text_fill = gameoverfont.render("K.O", True, (255,255,0)).convert_alpha()

            screen.blit(end_text_outline,(x+45,y-20))
            screen.blit(end_text_fill,(x+40, y-20))
            screen.blit(end_text_body,(x+35, y-20))
        



width = screen.get_width()
height = screen.get_height()


#instantiate fighters
fighter_1 = Fighter(200,350,"a","d","w","x","c","v",0,MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
fighter_2 = Fighter(700,350,"LEFT","RIGHT","UP","B","N","M",100,LIGHT_FIGHTER_DATA, light_fighter_sheet, light_animation_steps)


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
    fighter_1.move(width,height,screen,fighter_2)
    fighter_2.move(width,height,screen,fighter_1)

    #frame handling
    fighter_1.frame_handler()
    fighter_2.frame_handler()

    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if match_timer.active:
        match_timer.update()
    #check for end of match
    end_match(fighter_1.health, 400, 300)
    end_match(fighter_2.health, 400, 300)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update dislay
    pygame.display.update()

pygame.quit()