import pygame
class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up):
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0
        self.jump = False
        self.left = input_left
        self.right = input_right
        self.up = input_up
    def move(self,width,height):
        SPEED = 10
        GRAVITY = 1000
        dx = 0
        dy = 0
        #get keypresses
        key = pygame.key.get_pressed()

        #movement key presses
        if key[pygame.key.key_code(self.left)]:
            dx = - SPEED
        if key[pygame.key.key_code(self.right)]:
            dx = SPEED
        #jump
        if key[pygame.key.key_code(self.up)] and self.jump == False:
            self.vel_y = -30
            self.jump = True
        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
            #check screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > width:
            dx = width -self.rect.right
        if self.rect.bottom + dy > height - 60:
            self.rect_vel = 0
            self.jump = False
            dy = height - 60 - self.rect.bottom
        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self,surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)