
#errors i encountered x = didnt fix v = did! 
#x - when i attack whilst moving, become trapped in walking animation
#v - can move whilst hit
#v - interrupting attacks with an attack wouldnt play hit animation
#v - finisher meter goes to wrong person
#v - hit animation goes to other person
#v - hit animation would break other animations


import pygame
#to do:
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
        self.moving = False
        self.left = input_left
        self.right = input_right
        self.up = input_up
        self.health = health
        self.finisher_value = 0
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0#0: idle, 1: walk, 2: l_attack, 3: m_attack, 4: h_attack, 5: hit,6:death, 7: jump, 8: block
        self.update_time= pygame.time.get_ticks()
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.attack1 = attack1
        self.attack2 = attack2
        self.attack3 = attack3
        self.attack_type = 0
        self.flip = False
        self.attacking = False
        self.health_status = True
        self.attack_cooldown = 0
        self.hit = False

        

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
        SPEED = 7
        GRAVITY = 3
        dx = 0
        dy = 0
        self.moving = False
        self.attack_type = 0
        #get keypresses
        key = pygame.key.get_pressed()
        if self.attacking == False and self.hit == False:
            #movement key presses
            if key[pygame.key.key_code(self.left)]:
                dx = - SPEED
                self.moving = True
            if key[pygame.key.key_code(self.right)]:
                dx = SPEED
                self.moving = True
            if key[pygame.key.key_code(self.up)] and self.jump == False:
                self.vel_y = -30
                self.jump = True
                self.moving = False

            #attacking keys
            if not self.jump:
                if key[pygame.key.key_code(self.attack1)]:
                    self.attack_type = 1
                    #self.action_handler(2)
                    self.attack(surface,target)
                if key[pygame.key.key_code(self.attack2)]:
                    self.attack_type = 2
                    #self.action_handler(3)
                    self.attack(surface,target)
                if key[pygame.key.key_code(self.attack3)]:
                    self.attack_type = 3
                    #self.action_handler(4)
                    self.attack(surface,target)

              
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

        #apply attack cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -=1
    
    
    def frame_handler(self):
        #new method ensures that i restart the next action from the start of the frame index, stopping the index out of range error. 
        #must make sure that jump is before moving, otherwise when I jump it causes problems
        if self.hit == True:
            self.action_handler(5)
        elif self.jump == True:
            self.action_handler(7)
        elif self.moving == True:
            self.action_handler(1)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.action_handler(2)
            elif self.attack_type == 2:   
                self.action_handler(3)
            elif self.attack_type == 3:
                self.action_handler(4)
        else:
            self.action_handler(0)
        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 125
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action in [2,3,4]:
                    self.attacking = False
                    self.attack_cooldown = 10
                if self.hit == True:
                    self.hit = False
                    #interrupt attack if attacked during wind up
                    self.attacking = False
                    self.attack_cooldown = 10
                
            
    def action_handler(self,new_action):
        #check if new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            #reset the frame index
            self.frame_index = 0
            #reset the update time
            self.update_time = pygame.time.get_ticks()
    
    def finisher_meter(self,finisher_value):
        if self.finisher_value < 200:
            self.finisher_value += 20
    
    def attack(self,surface,target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_hitbox = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y,2 * self.rect.width+100, self.rect.height)
            if attack_hitbox.colliderect(target.rect):
                target.damage(10)
                self.finisher_meter(10)
                target.hit = True
                print("hit")
                print(target.health)
        
        
        #pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt):
        self.health -= damage_dealt
        if self.health <= 0:
            self.action_handler(6)

    def draw(self,surface):
        #have to create a seperate flip image (img) so that players face each other if they pass
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,255,255), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
