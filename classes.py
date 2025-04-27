import pygame
import csv

# Initialize Pygame modules
pygame.init()

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
        self.colour_normal = colour_dark
        self.colour_hover = colour_light
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

class Leaderboard:
    def __init__(self, file_path="name.csv"):
        self.file_path = file_path

    def get_sorted_leaderboard(self):
        try:
            with open(self.file_path, mode="r") as file:
                reader = csv.reader(file)
                leaderboard = sorted(reader, key=lambda x: int(x[1]))  # Sort by time (second column)
                return leaderboard
        except FileNotFoundError:
            print("Leaderboard file not found.")
            return []

    def display_top_5(self, screen, x, y):
        leaderboard = self.get_sorted_leaderboard()
        font = pygame.font.Font('files/mini_pixel-7.ttf', 30)
        title_surf = font.render("Top 5 Fastest Times", True, (255, 255, 255))
        screen.blit(title_surf, (x, y))

        for i, entry in enumerate(leaderboard[:5], start=1):
            name, time = entry
            entry_surf = font.render(f"{i}. {name}: {time} seconds", True, (255, 255, 255))
            screen.blit(entry_surf, (x, y + 40 * i))

def play_sound_effect(sound):
    if settings["sound_effects_on"]:
        sound.play()
