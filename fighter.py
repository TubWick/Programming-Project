import pygame
#to do:
#directional attack - if facing left attack left and vice versa
#find sprites
#Healthbar: rectangle, whenever damage tkan it gets smaller
 #each attack has different damages - three types of attack - damage will vary depending of character class
#       light attack - will be a light jab with little knockback and closer range - good for starting combos
#       medium attack - will be a punch with some knockback - slightly larger range so connecting will be easier
#       heavy attack - will be an attack with a lot of knockback - large range but slower to execute
#






class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3,health, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0
        self.jump = False
        self.left = input_left
        self.right = input_right
        self.up = input_up
        self.health = health
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0#0: idle, 1: walk, 2: jump, 3: attack1, 4: attack2, 5: attack3, 6: hit, 7: death
        self.update_time= pygame.time.get_ticks()
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.attack1 = attack1
        self.attack2 = attack2
        self.attack3 = attack3
        self.flip = False
        self.attacking = False

    def load_images(self,sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y*self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


    def move(self,width,height,surface,target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        #get keypresses
        key = pygame.key.get_pressed()
        if self.attacking == False:
            #movement key presses
            if key[pygame.key.key_code(self.left)]:
                dx = - SPEED
            if key[pygame.key.key_code(self.right)]:
                dx = SPEED
            if key[pygame.key.key_code(self.up)] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            #attacking keys
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
    
    
    def frame_handler(self):
        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 250
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                self.attacking = False
                self.action = 0
    
    
    def attack(self,surface,target):
        self.attacking = True
        attack_hitbox = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y,2 * self.rect.width, self.rect.height)
        if attack_hitbox.colliderect(target.rect):
            target.damage(10)
            print("hit")
            print(target.health)
        pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt):
        self.health -= damage_dealt

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255,255,255), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
