import pygame
colour = (0, 0, 0)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)

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
        self.colour_normal = (255,0,0)
        self.colour_hover = (0,255,0)
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
        if self.get_hovered() and self.action and pygame.mouse.get_pressed()[0]:
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
