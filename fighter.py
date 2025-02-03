import pygame
#to do:
#directional attack - if facing left attack left and vice versa
#find sprites or 7ups 
#Healthbar: rectangle, whenever damage tkan it gets smaller
#once healthbar - complete damage method
#each attack has different damages - three types of attack - damage will vary depending of character class





class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3):
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0
        self.jump = False
        self.left = input_left
        self.right = input_right
        self.up = input_up
        self.health = 100
        self.attack1 = attack1
        self.attack2 = attack2
        self.attack3 = attack3
        self.flip = False
    def move(self,width,height,surface,target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        #get keypresses
        key = pygame.key.get_pressed()

        #movement key presses
        if key[pygame.key.key_code(self.left)]:
            dx = - SPEED
        if key[pygame.key.key_code(self.right)]:
            dx = SPEED
        if key[pygame.key.key_code(self.up)] and self.jump == False:
            self.vel_y = -30
            self.jump = True
        


        #attack keys
        if key[pygame.key.key_code(self.attack1)]:
            self.attack(surface,target)
            #print("attack1 used!!!!")
        if key[pygame.key.key_code(self.attack2)]:
            self.attack(surface,target)
            #print("attack2 used!!!!")
        if key[pygame.key.key_code(self.attack3)]:
            self.attack(surface,target)
            #print("attack3 used!!!!")

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
        
        #check players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self,surface,target):
        attack_hitbox = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y,2 * self.rect.width, self.rect.height)
        if attack_hitbox.colliderect(target.rect):
            print("hit")
            
        pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt):
        self.health -= damage_dealt

    def draw(self,surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)