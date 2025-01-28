import pygame
from fighter import Fighter

pygame.init()
#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption = ("Fighting game")

#create background image
bg_image= pygame.image.load("files/assets/background.png").convert_alpha()

#set framerate
clock = pygame.time.Clock()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (width,height))
    screen.blit(scaled_bg, (0,0))

width = screen.get_width()
height = screen.get_height()


#instantiate fighters
fighter_1 = Fighter(200,350)
fighter_2 = Fighter(700,350)



#game loop
run = True
while run:

    clock.tick(60)

    #draw background
    draw_bg()

    #move fighters
    fighter_1.move()
    fighter_2.move()
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