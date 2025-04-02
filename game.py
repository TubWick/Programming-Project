#errors
#x - can still type more than 2 chars
#v - letters vanished moment they appeared - pass input_text as param
#v - not going to new line in csv file 



import pygame
from fighter import Fighter
from characterselection import Charselectionscreen
from pygame import mixer
import csv

mixer.init()
pygame.init()

lighticon = pygame.image.load("files/assets/lighticon.png").convert_alpha()
mediumicon = pygame.image.load("files/assets/mediumicon.png").convert_alpha()
heavyicon = pygame.image.load("files/assets/heavyicon.png").convert_alpha()
lighticon = pygame.transform.scale(lighticon, (400, 450))
mediumicon = pygame.transform.scale(mediumicon, (400, 450))
heavyicon = pygame.transform.scale(heavyicon, (400, 450))

match_end_time = 0
match_end_trigger = False

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



smallfont = pygame.font.Font('files/mini_pixel-7.ttf',100)
errorfont = pygame.font.Font('files/Game Paused DEMO.ttf',50)
gameoverfont = pygame.font.Font('files/mini_pixel-7.ttf',150)
winscreenfont = pygame.font.Font('files/mini_pixel-7.ttf',125)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)
input_box = pygame.Rect(200,200,150, 100)
input_text = ""  # The text the user types
input_active = False 
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
light_animation_steps = [4,5,2,2,3,1,5,3,1,6]
medium_animation_steps  = [4,6,2,3,3,1,5,3,1,4]
heavy_animation_steps =   [4,4,3,3,3,1,4,3,1,6]
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
    global match_end_time
    global match_end_trigger
    if health <= 0:
        if match_end_time == 0:
            match_end_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        flash_duration = 500
        #takes the current time, divs it by 2 t get either 2 or a 1, and then mod it by 2 to get a one or a 0
        #eg: 500(ms currentime) // 500(flashduration) % 2 = 1  
        if match_end_trigger == False and current_time // flash_duration % 2 == 0: 
            end_text_body = gameoverfont.render("K.O", True, ((255,10,20))).convert_alpha()
            end_text_outline = gameoverfont.render("K.O", True, (0,0,0)).convert_alpha()
            end_text_fill = gameoverfont.render("K.O", True, (255,255,0)).convert_alpha()
            screen.blit(end_text_outline,(x+45,y-20))
            screen.blit(end_text_fill,(x+40, y-20))
            screen.blit(end_text_body,(x+25, y-15))

def win_screen(x,y,text_colour):
    global input_box
    global input_text 
    global input_active  
    screen.fill((0,0,0))
    win_text_body = winscreenfont.render("PLAYER X WINS", True, ((255,10,20))).convert_alpha()
    win_text_outline = winscreenfont.render("WIN", True, (0,0,0)).convert_alpha()
    screen.blit(win_text_outline,(x+45,y-120))
    screen.blit(win_text_body,(x-250, y-300)) 
    screen.blit(heavyicon, (x + 120, y - 175))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
                print("selected")
                
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(input_text)<=0 or len(input_text) > 2:
                    print("cant be empty or more than 2")
                # error = errorfont.render("Input Cannot Be Empty", True, (255,255,255)).convert_alpha()
                 #   screen.blit(error, (200, 150))
                else:
                    with open("name.csv", mode="a",newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([input_text])
                    print(f"User typed: {input_text}")  
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
            
    pygame.draw.rect(screen, (255, 255, 255), input_box)
    text_surface = smallfont.render(input_text, True, (0,0,255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))


width = screen.get_width()
height = screen.get_height()

#instantiate fighters

fighter_1 = Fighter(200,350,"a","d","w","x","c","v","f",100,MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
fighter_2 = Fighter(700,350,"LEFT","RIGHT","UP","B","N","M","l",100,LIGHT_FIGHTER_DATA, light_fighter_sheet, light_animation_steps)


#game loop
run = True
while run:
    clock.tick(60)

    # Retrieve all events once per frame
    events = pygame.event.get()

    #draw background
    draw_bg()
    
    #show player health
    draw_healthbar(fighter_1.health, 20, 20)
    draw_healthbar(fighter_2.health, 580, 20)
   
    #draw player finisher
    draw_finisherbar(fighter_1.finisher_value, 20, 60)
    draw_finisherbar(fighter_2.finisher_value, 780, 60)

    #frame handling
    fighter_1.frame_handler()
    fighter_2.frame_handler()

    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #move fighters
    fighter_1.move(width, height, screen, fighter_2, events)
    fighter_2.move(width, height, screen, fighter_1, events)

    if match_timer.active:
        match_timer.update()
    
    if match_end_time != 0:
        if pygame.time.get_ticks() - match_end_time >0000:
            match_end_trigger = True
            win_screen(400,300,((255,255,255)))
            
            pygame.display.update()

    #check for end of match
    end_match(fighter_1.health, 400, 300)
    end_match(fighter_2.health, 400, 300)

    #event handler
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()