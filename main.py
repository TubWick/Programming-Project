import pygame
import sys
import os
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

smallfont = pygame.font.Font('files/mini_pixel-7.ttf',50)
shenttpuro = pygame.font.Font('files/Shenttpuro Font.ttf',100)
text_surf = shenttpuro.render( 'First Strike',True, (255, 10, 10) )
screen_state = 0

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
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.lbfont = pygame.font.Font('files/mini_pixel-7.ttf', 70)
        self.lbwidth = 400
        self.lbheight = 600
    def draw_leaderboard(self):
        backbutton.imagedraw()
        leaderboard_rect=pygame.Rect((self.x // 2 - self.lbwidth//2, self.y //2 - self.lbheight//2),(self.lbwidth, self.lbheight))
        pygame.draw.rect(screen,(colour_dark),leaderboard_rect)
        lbtitlesurf = self.lbfont.render('Leaderboard',True,(255,255,255))
        screen.blit(lbtitlesurf,(self.x // 2 - lbtitlesurf.get_width()//2, self.y // 2 - self.lbheight // 2))

#button actions changing screenstate

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
                                                                                            #120

# instantiations
startbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 120, button_width, button_height, "Start", start_action)
settingsbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 60, button_width, button_height, "Settings", settings_action)
leaderboardbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2, button_width, button_height, "Leaderboard", leaderboard_action)
leaderboard = Leaderboard(width,height)
quitbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 + 60, button_width, button_height, "Quit", quit_action)
backbutton = BackButton(10,10,width,height,lambda: back_button.backaction())
characterselection = Charselectionscreen(500, 200)
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
    
    #main menu
    if screen_state == 0:
        quitbutton.draw(screen)
        leaderboardbutton.draw(screen)
        settingsbutton.draw(screen)
        startbutton.draw(screen)
        text_rect = text_surf.get_rect(center=(width // 2, height // 4 - 50))
        screen.blit(text_surf, text_rect)
        print("my heart goes out to you")
    #settings
    if screen_state == 1:
        backbutton.imagedraw()
        backbutton.backaction()
        settingsbutton.draw(screen)
    #leaderboard
    if screen_state == 2:
        backbutton.imagedraw()
        backbutton.backaction()
        leaderboard.draw_leaderboard()
    #main game
    if screen_state == 3:
        print(screen_state)
        characterselection.draw_cs_screen()
        characterselection.ifhover()
        characterselection.ifclicked(event)
        characterselection.draw_selected_outline()
        backbutton.imagedraw()
        backbutton.backaction()

        

    pygame.display.update()


pygame.quit()
sys.exit()