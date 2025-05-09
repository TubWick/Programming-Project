#errors
#x - can still type more than 2 chars
#v - letters vanished moment they appeared - pass input_text as param
#v - not going to new line in csv file 

#to do
# the player that wins gets saved to a vatriable 
# can get passed throigh to this file
# that can then determine which player won and the icon it blits by using p1_selected!!!
# kills two birds with one stone


import pygame
from fighter import Fighter
from characterselection import Charselectionscreen
from pygame import mixer
import csv
from classes import Button, Leaderboard  # Update import to use classes
import os
import shared_state  # Import the shared state module
import sys


def mainmenu_action():
    pygame.display.quit()
    os.system("python main.py")

 
mainmenu_button= Button(10,10,100,100, "Main Menu", lambda: mainmenu_action())

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
        self.total_match_time = None  # Store the total match time when the timer stops

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.total_match_time = None  # Reset total match time when reactivated

    def deactivate(self):
        if self.active:
            self.active = False
            self.total_match_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Record match time
            self.start_time = 0

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) // 1000
            time_surf = smallfont.render(str(elapsed_time), True, (255, 255, 255)).convert_alpha()
            time_surf_outline = smallfont.render(str(elapsed_time), True, (0, 0, 0)).convert_alpha()
            screen.blit(time_surf_outline, (width // 2 - 7, height // 2 - 297))
            screen.blit(time_surf, (width // 2 - 10, height // 2 - 300))

match_timer = Timer()
match_timer.activate()


#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption("Fighting game")

smallfont = pygame.font.Font('files/mini_pixel-7.ttf',100)
errorfont = pygame.font.Font('files/Game Paused DEMO.ttf',30)
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

# Initialize global variables
valid_input_made = False  # Fix: Initialize valid_input_made
error_message = ""  # Initialize error_message

def restart_match():
    global fighter_1, fighter_2, match_timer, match_end_time, match_end_trigger
    # Reinitialize fighters
    fighters.InitialiseFighters()
    fighter_1 = fighters.fighter_1
    fighter_2 = fighters.fighter_2
    # Reset match timer and end conditions
    match_timer.activate()
    match_end_time = 0
    match_end_trigger = False

def confirm_quit():
    # Confirmation dialog for quitting
    confirm = True
    while confirm:
        screen.fill((0, 0, 0))
        confirm_text = gameoverfont.render("Are you sure?", True, (255, 255, 255))
        yes_button = Button(width // 2 - 150, height // 2 + 10, 100, 50, "Yes", lambda: sys.exit())  # Moved down by 10 pixels
        no_button = Button(width // 2 + 50, height // 2 + 10, 100, 50, "No", lambda: False)  # Moved down by 10 pixels

        screen.blit(confirm_text, (width // 2 - confirm_text.get_width() // 2, height // 2 - 100))
        yes_button.draw(screen)
        no_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.get_hovered():
                    yes_button.click()
                elif no_button.get_hovered():
                    confirm = False

        pygame.display.update()

def pause_menu():
    paused = True
    resume_button = Button(width // 2 - 100, height // 2 - 80, 200, 50, "Resume", lambda: False)  # Moved down by 20 pixels
    restart_button = Button(width // 2 - 100, height // 2 - 20, 200, 50, "Restart", restart_match)  # Moved down by 20 pixels
    main_menu_button = Button(width // 2 - 100, height // 2 + 40, 200, 50, "Main Menu", mainmenu_action)  # Moved down by 20 pixels
    quit_button = Button(width // 2 - 100, height // 2 + 100, 200, 50, "Quit", confirm_quit)  # Moved down by 20 pixels

    while paused:
        screen.fill((0, 0, 0))
        pause_text = gameoverfont.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 200))

        # Draw buttons
        resume_button.draw(screen)
        restart_button.draw(screen)
        main_menu_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.get_hovered():
                    paused = resume_button.click()
                elif restart_button.get_hovered():
                    restart_button.click()
                    paused = False
                elif main_menu_button.get_hovered():
                    main_menu_button.click()
                elif quit_button.get_hovered():
                    quit_button.click()

        pygame.display.update()

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
            match_timer.deactivate()  # Pause the timer and record the match time
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
            screen.blit(end_text_body,(x+35, y-20))

def win_screen(x, y, text_colour):
    global input_box
    global input_text 
    global input_active  
    global mainmenu_button
    global valid_input_made  # Ensure valid_input_made is global
    global error_message  # Ensure error_message is global

    screen.fill((0, 0, 0))

    # Check for Player 1 win
    if fighter_1.winner == "Player 1" or fighter_2.winner == "Player 1":
        win_text_body = winscreenfont.render("PLAYER 1 WINS", True, ((255, 10, 20))).convert_alpha()
        if p1_selected == "light":
            screen.blit(lighticon, (x + 120, y - 175))
        elif p1_selected == "medium":
            screen.blit(mediumicon, (x + 120, y - 175))
        elif p1_selected == "heavy":
            screen.blit(heavyicon, (x + 120, y - 175))

    # Check for Player 2 win
    elif fighter_1.winner == "Player 2" or fighter_2.winner == "Player 2":
        win_text_body = winscreenfont.render("PLAYER 2 WINS", True, ((255, 10, 20))).convert_alpha()
        if p2_selected == "light":
            screen.blit(lighticon, (x + 120, y - 175))
        elif p2_selected == "medium":
            screen.blit(mediumicon, (x + 120, y - 175))
        elif p2_selected == "heavy":
            screen.blit(heavyicon, (x + 120, y - 175))

    else:
        # Default value for win_text_body in case no winner is detected
        win_text_body = winscreenfont.render("NO WINNER", True, ((255, 255, 255))).convert_alpha()

    # Display the winner text
    screen.blit(win_text_body, (x - 250, y - 300))

    # Display match time
    if match_timer.total_match_time is not None:
        time_text = smallfont.render(f"Time: {match_timer.total_match_time} seconds", True, (255, 255, 255))
        screen.blit(time_text, (x - 150, y - 200))

    # Handle input for saving player initials
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN and not valid_input_made:
            if event.key == pygame.K_RETURN:
                if len(input_text) <= 0:
                    error_message = "Input cannot be blank"
                elif len(input_text) > 2:
                    error_message = "Input has to be less than two characters"
                else: 
                    
                    with open("name.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([input_text, match_timer.total_match_time])  # Save name and time
                        print(f"Time: {match_timer.total_match_time}")  # Debugging
                    valid_input_made = True  # Mark valid input as made
                    error_message = ""  # Clear the error message
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Draw input box for initials
    if not valid_input_made:
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        text_surface = smallfont.render(input_text, True, (0, 0, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Display error message if any
        if error_message:
            error_surface = errorfont.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (input_box.x, input_box.y + 110))
    else:
        # Show main menu button only after valid input
        mainmenu_button.draw(screen)
        mainmenu_button.click()

width = screen.get_width()
height = screen.get_height()

class CreateFighters:
    def __init__(self, p1_character, p2_character):
        self.p1_character = p1_character
        self.p2_character = p2_character
        self.fighter_1 = None  # Initialize as None
        self.fighter_2 = None  # Initialize as None

    def InitialiseFighters(self):
        print(f"Player 1 selected: {self.p1_character}")
        print(f"Player 2 selected: {self.p2_character}")
        if self.p1_character == "light":
            self.fighter_1 = Fighter(200, 350, "a", "d", "w", "x", "c", "v", "f",100, LIGHT_FIGHTER_DATA, light_fighter_sheet, light_animation_steps)
        elif self.p1_character == "medium":
            self.fighter_1 = Fighter(200, 350, "a", "d", "w", "x", "c", "v", "f", 100, MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
        elif self.p1_character == "heavy":
            self.fighter_1 = Fighter(200, 350, "a", "d", "w", "x", "c", "v", "f", 100, HEAVY_FIGHTER_DATA, heavy_fighter_sheet, heavy_animation_steps)
        if self.p2_character == "light":
            self.fighter_2 = Fighter(700, 350, "LEFT", "RIGHT", "UP", "B", "N", "M", "l", 100, LIGHT_FIGHTER_DATA, light_fighter_sheet, light_animation_steps)
        elif self.p2_character == "medium":
            self.fighter_2 = Fighter(700, 350, "LEFT", "RIGHT", "UP", "B", "N", "M", "l", 100, MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
        elif self.p2_character == "heavy":
            self.fighter_2 = Fighter(700, 350, "LEFT", "RIGHT", "UP", "B", "N", "M", "l", 100, HEAVY_FIGHTER_DATA, heavy_fighter_sheet, heavy_animation_steps)

# Read selected characters from the file
try:
    with open("selected_characters.txt", "r") as file:
        p1_selected = file.readline().strip()
        p2_selected = file.readline().strip()
except FileNotFoundError:
    print("Error: Selected characters file not found.")
    pygame.quit()
    sys.exit()

if not p1_selected or not p2_selected:
    print("Error: One or both players did not select a character.")
    pygame.quit()
    sys.exit()

print(f"Player 1 selected: {p1_selected}")
print(f"Player 2 selected: {p2_selected}")

# Ensure selected characters are valid before initializing fighters
fighters = CreateFighters(p1_selected, p2_selected)
fighters.InitialiseFighters()

# Access fighters globally
fighter_1 = fighters.fighter_1
fighter_2 = fighters.fighter_2

if not fighter_1 or not fighter_2:
    print("Error: Fighters could not be initialized.")
    pygame.quit()
    sys.exit()


#game loop
run = True
while run:
    clock.tick(60)

    # Retrieve all events once per frame to allow for perfect parryies
    events = pygame.event.get()

        #event handler
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()

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

    # Update timer
    if match_timer.active and not match_end_trigger:
        match_timer.update()

    if match_end_time != 0:
        if pygame.time.get_ticks() - match_end_time > 5000:
            match_end_trigger = True
            if fighter_1.winner or fighter_2.winner:
                winner = fighter_1.winner or fighter_2.winner  # Get the winner
                print(f"Winner detected: {winner}")  # Debugging
                win_screen(400, 300, ((255, 255, 255)))
            else:
                print("No winner detected.")  # Debugging
                win_screen(400, 300, ((255, 255, 255)))
            pygame.display.update()
          
    #check for end of match
    end_match(fighter_1.health, 400, 300)
    end_match(fighter_2.health, 400, 300)



    #update display
    pygame.display.update()

pygame.quit()