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
        
            screen.blit(time_surf_outline,(width//2 + 2, height//2 + 2))
            screen.blit(time_surf,(width//2, height//2))

match_timer = Timer()
match_timer.activate()
#i need a plain black background
def draw_bg():
    width = screen.get_width()
    height = screen.get_height()
    screen.fill((0,255,0))


#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption("Fighting game")

smallfont = pygame.font.Font('files/mini_pixel-7.ttf',75)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)

width = screen.get_width()
height = screen.get_height()

clock = pygame.time.Clock()
#game loop
run = True
while run:
    clock.tick(60)
    #draw background
    draw_bg()
    
        
    if match_timer.active:
        match_timer.update()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update dislay
    pygame.display.update()

pygame.quit()