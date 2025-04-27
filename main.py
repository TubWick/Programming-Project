import pygame
import sys
import os
import csv  # Fix: Import the csv module
from pygame import mixer
import shared_state  # Import the shared state module

mixer.init()
pygame.init()
from characterselection import Charselectionscreen
res = 1280,720
screen = pygame.display.set_mode((res))
colour = (0, 0, 0)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)

width = screen.get_width()
height = screen.get_height()

button_width = 220
button_height = 50

smallfont = pygame.font.Font('files/mini_pixel-7.ttf', 50)  
shenttpuro = pygame.font.Font('files/Shenttpuro Font.ttf', 120)  
text_surf = shenttpuro.render('First Strike', True, (255, 10, 10))
screen_state = 0

# Global settings state
settings = {
    "music_on": True,
    "sound_effects_on": True
}

def toggle_music():
    settings["music_on"] = not settings["music_on"]
    if settings["music_on"]:
        mixer.music.unpause()
    else:
        mixer.music.pause()

def toggle_sound_effects():
    settings["sound_effects_on"] = not settings["sound_effects_on"]

#classes
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height  
        self.text = text
        self.action = action
        self.colour_normal = colour_light
        self.colour_hover = colour_dark
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
    #draw button
    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, self.colour_hover, [self.x, self.y, self.width, self.height])
        else:
            pygame.draw.rect(screen, self.colour_normal, [self.x, self.y, self.width, self.height])

        text_surf = smallfont.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surf, text_rect)
    # if button hovered
    def get_hovered(self):
        mouse = pygame.mouse.get_pos()
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def click(self):
        if self.get_hovered() and self.action:
            self.action()

class BackButton(Button):
    def __init__(self,x,y,width,height,action):
        super().__init__(x,y,width,height,action)
        self.back_img =pygame.transform.scale_by (pygame.image.load('files/assets/backarrow.png'),4)
        self.rect = self.back_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def backaction(self):
        global screen_state
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            screen_state = 0
    def imagedraw(self):
        screen.blit(self.back_img,(self.rect.x,self.rect.y))

#class leaderboard
#open to csv
#add the score to the list of scores in the csv
#sort the scores - use bubble sort
#draw the list
#lb = leaderboard

class Leaderboard:
    def __init__(self, x, y, file_path="name.csv"):
        self.x, self.y = x, y
        self.file_path = file_path
        self.lbfont = pygame.font.Font('files/mini_pixel-7.ttf', 50)  # Separate font instance for leaderboard
        self.lbwidth = 400
        self.lbheight = 600

    def get_sorted_leaderboard(self):
        try:
            with open(self.file_path, mode="r") as file:
                reader = csv.reader(file)
                leaderboard = [row for row in reader if len(row) == 2 and row[1].isdigit()]  # Validate rows
                leaderboard = sorted(leaderboard, key=lambda x: int(x[1]))  # Sort by time
                return leaderboard
        except FileNotFoundError:
            print("Leaderboard file not found.")
            return []

    def draw_leaderboard(self, screen):
        backbutton.imagedraw()
        leaderboard_rect = pygame.Rect((self.x // 2 - self.lbwidth // 2, self.y // 2 - self.lbheight // 2), (self.lbwidth, self.lbheight))
        pygame.draw.rect(screen, colour_dark, leaderboard_rect)
        lbtitlesurf = self.lbfont.render('Leaderboard', True, (255, 255, 255))
        screen.blit(lbtitlesurf, (self.x // 2 - lbtitlesurf.get_width() // 2, self.y // 2 - self.lbheight // 2 + 10))

        leaderboard = self.get_sorted_leaderboard()
        for i, entry in enumerate(leaderboard[:5], start=1):
            name, time = entry
            entry_surf = self.lbfont.render(f"{i}. {name}: {time} seconds", True, (255, 255, 255))
            screen.blit(entry_surf, (self.x // 2 - self.lbwidth // 2 + 20, self.y // 2 - self.lbheight // 2 + 50 + i * 60))  # Adjusted spacing

#button action changing screenstate

def quit_action():
    global screen_state
    global running
    print("screen_state: ", screen_state)
    pygame.quit()
    sys.exit()

def settings_action():
    global screen_state
    screen_state = 1

def leaderboard_action():
    global screen_state
    screen_state = 2

def start_action():
    global screen_state
    screen_state = 3

def start_match_action():
    global screen_state
    if characterselection.p1_selected and characterselection.p2_selected:
        # Save selected characters to a file
        with open("selected_characters.txt", "w") as file:
            file.write(f"{characterselection.p1_selected}\n")
            file.write(f"{characterselection.p2_selected}\n")
        print("Saved P1:", characterselection.p1_selected, "P2:", characterselection.p2_selected)
        # Launch game.py and exit main.py
        pygame.quit()
        os.system("python game.py")
        sys.exit()  # Exit main.py
    else:
        print("Both players must select their characters before starting the match.")

# Update settings screen
def draw_settings_menu():
    global screen_state
    backbutton.imagedraw()
    backbutton.backaction()

    # Create buttons for toggling music and sound effects
    music_button = Button(
        width // 2 - button_width // 2,
        height // 2 - button_height // 2 - 60,
        button_width,
        button_height,
        f"Music: {'On' if settings['music_on'] else 'Off'}",
        toggle_music
    )
    sound_effects_button = Button(
        width // 2 - button_width // 2,
        height // 2 - button_height // 2 + 20,
        button_width,
        button_height,
        f"Sound Effects: {'On' if settings['sound_effects_on'] else 'Off'}",
        toggle_sound_effects
    )

    # Draw buttons
    music_button.draw(screen)
    sound_effects_button.draw(screen)

    # Add a title for the settings menu
    settings_title = smallfont.render("Settings", True, (255, 255, 255))  # Use smallfont here
    screen.blit(settings_title, (width // 2 - settings_title.get_width() // 2, height // 2 - button_height // 2 - 150))

# instantiations
startbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 100, button_width, button_height, "Start", start_action)  # Moved down by 20 pixels
settingsbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 40, button_width, button_height, "Settings", settings_action)  # Moved down by 20 pixels
leaderboardbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 + 20, button_width, button_height, "Leaderboard", leaderboard_action)  # Moved down by 20 pixels
quitbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 + 80, button_width, button_height, "Quit", quit_action)  # Moved down by 20 pixels
backbutton = BackButton(10,10,width,height,lambda: back_button.backaction())
startmatchbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 + 320, button_width, button_height, "Start Match", start_match_action)  # Moved down by 20 pixels
characterselection = Charselectionscreen(500, 200)
leaderboard = Leaderboard(width,height)
# main game loop
running = True
while running:
    screen.fill(colour)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #event handling for buttons
        if screen_state == 0:
                if quitbutton.get_hovered():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        quitbutton.click()
                elif settingsbutton.get_hovered(): 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        settingsbutton.click()
                elif startbutton.get_hovered():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        startbutton.click()
                elif leaderboardbutton.get_hovered():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        leaderboardbutton.click()
        elif screen_state == 3:
            if startmatchbutton.get_hovered():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    startmatchbutton.click()
    
    #main menu
    if screen_state == 0:
        quitbutton.draw(screen)
        leaderboardbutton.draw(screen)
        settingsbutton.draw(screen)
        startbutton.draw(screen)
        text_rect = text_surf.get_rect(center=(width // 2, height // 4 - 50))
        screen.blit(text_surf, text_rect)
        
    #settings
    if screen_state == 1:
        draw_settings_menu()
    #leaderboard
    if screen_state == 2:
        backbutton.imagedraw()
        backbutton.backaction()
        leaderboard = Leaderboard(width, height, "name.csv")  # Pass file path
        leaderboard.draw_leaderboard(screen)  # Draw the leaderboard
    #main game
    if screen_state == 3:
      #  print(screen_state)
        characterselection.draw_cs_screen()
        characterselection.ifhover()
        characterselection.ifclicked(event)
        characterselection.draw_selected_outline()
        backbutton.imagedraw()
        backbutton.backaction()
        startmatchbutton.draw(screen)

    pygame.display.update()


pygame.quit()
sys.exit()

from classes import Leaderboard

def show_leaderboard():
    leaderboard = Leaderboard()
    leaderboard.display_top_5()


show_leaderboard()