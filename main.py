import pygame

pygame.init()

res = (1080, 1080)
screen = pygame.display.set_mode(res)
colour = (0, 0, 0)
colour_light = (100, 100, 100)
colour_dark = (170, 170, 170)

width = screen.get_width()
height = screen.get_height()

button_width = 220
button_height = 50

smallfont = pygame.font.Font('files/mini_pixel-7.ttf',50)
shenttpuro = pygame.font.Font('files/Shenttpuro Font.ttf',100)
text_surf = shenttpuro.render( 'First Strike',True, (255, 10, 10) )

screen_state = 0

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.colour_normal = colour_dark
        self.colour_hover = colour_light
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, self.colour_hover, [self.x, self.y, self.width, self.height])
        else:
            pygame.draw.rect(screen, self.colour_normal, [self.x, self.y, self.width, self.height])

        text_surf = smallfont.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surf, text_rect)

    def get_hovered(self):
        mouse = pygame.mouse.get_pos()
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def click(self):
        if self.get_hovered() and self.action:
            self.action()

class BackButton(Button):
    def __init__(self,x,y,width,height,action):
        super().__init__(x,y,width,height,action)
        self.back_img =pygame.transform.scale_by (pygame.image.load('files/backarrow.png'),4)
        self.rect = self.back_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def backaction(self):
        global screen_state
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            screen_state = 0
    def imagedraw(self):
        screen.blit(self.back_img,(self.rect.x,self.rect.y))

from leaderboard import highscore
Highscore = highscore(width,height,lambda:Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 60, button_width, button_height,"leaderboard"),screen)


def quit_action():
    pygame.quit()

def settings_action():
    global screen_state
    screen_state = 1
    print("screen state changed to", screen_state)

def leaderboardaction():
    global screen_state
    screen_state = 2


# button obj
startbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 180, button_width, button_height, "Start", quit_action)
settingsbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 120, button_width, button_height, "Settings", settings_action)
leaderboardbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 - 60, button_width, button_height, "Leaderboard", leaderboardaction) 
quitbutton = Button(width // 2 - button_width // 2, height // 2 - button_height // 2 , button_width, button_height, "Quit", quit_action)
backbutton = BackButton(10,10,width,height,lambda: back_button.backaction())
# game loop
running = True
while running:
    screen.fill(colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
                if quitbutton.get_hovered():
                    quitbutton.click()
                elif settingsbutton.get_hovered(): 
                    settingsbutton.click()
                elif startbutton.get_hovered():
                    startbutton.click()
                elif leaderboardbutton.get_hovered(): 
                    leaderboardaction()

    if screen_state == 0:
        quitbutton.draw(screen)
        leaderboardbutton.draw(screen)
        settingsbutton.draw(screen)
        startbutton.draw(screen)
        text_rect = text_surf.get_rect(center=(width // 2, height // 4 - 50))
        screen.blit(text_surf, text_rect)
        
    if screen_state == 1:
        quitbutton.draw(screen)
        backbutton.imagedraw()
        backbutton.backaction()
    if screen_state == 2:
        backbutton.imagedraw()
        backbutton.backaction()
    pygame.display.update()

pygame.quit()



















#class leaderboard
#open to csv
#add the score to the list of scores in the csv
#sort the scores - use bubble sort
#draw the list
#lb = leaderboard

class Leaderboard(self,x,y):
    self.x,self.y = x,y
    self.lbcolour = (255,255,255)
    self.lbfont = 'files/mini_pixel-7.ttf'
def draw_leaderboard(self):
    screen.fill(0,0,0)
    backbutton.imagedraw()
    leaderboard_rect=pygame.Rect((screen.get_width()//2-self.max/1.5,screen.get_height()//2-(self.max_height*4)),(self.max+10,(self.max_height*5)))
    pygame.draw.rect(screen,(0,173,212),highscore_rect)


