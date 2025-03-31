import pygame

#errors i encountered x = didnt fix v = did! 
#v - when i attack whilst moving, become trapped in walking animation
#v/x - can move whilst hit
#v - interrupting attacks with an attack wouldnt play hit animation
#v - finisher meter goes to wrong person
#v - hit animation goes to other person
#v - hit animation would break other animations
#v - attacking a blocking fighter sometimes locks person who attacks the blocking fighter into walking animation
#x - parry window is not working - attacks cannot be parried
#x - 

#to do
 #each attack has different damages - three types of attack - damage will vary depending of character class
# v      light attack - will be a light jab with little knockback and closer range - good for starting combos
# v      medium attack - will be a punch with some knockback - slightly larger range so connecting will be easier
# v      heavy attack - will be an attack with a lot of knockback - large range but slower to execute
# x      finisher - will be a powerful attack that can only be used when the finisher meter is full 
# x      parry - will be a defensive move that can be used if you block an attack quickly, will grant significant finisher meter if you know the timing
# v      blocking - will be a defensive move that negates damage taken from attacks, can be broken by heavy attacks


class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3,block,health, data, sprite_sheet, animation_steps):
        self.parry_window = False
        self.parry_timer = 0
        self.parry_duration = 3000
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect((x,y,80,180))
        self.block_effect = pygame.image.load("files/assets/dustcloud.png").convert_alpha()
        self.block_effect = pygame.transform.scale(self.block_effect, (100, 100))
        self.parry_effect = pygame.image.load("files/assets/parry_icon.png").convert_alpha()
        self.parry_effect = pygame.transform.scale(self.parry_effect, (200, 200))  # Scale parry effect correctly
        self.vel_y = 0
        self.jump = False
        self.moving = False
        self.blocking = False
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
        self.block = block
        self.attack_type = 0
        self.flip = False
        self.attacking = False
        self.health_status = True
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True
        #load audio
        pygame.mixer.music.load("files/audio/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) 
        self.light_attack_sound = pygame.mixer.Sound("files/audio/lighthit.wav")
        self.light_attack_sound.set_volume(0.5)
        self.medium_attack_sound = pygame.mixer.Sound("files/audio/mediumhit.wav")
        self.medium_attack_sound.set_volume(0.5)
        self.heavy_attack_sound = pygame.mixer.Sound("files/audio/heavyhit.wav")
        self.heavy_attack_sound.set_volume(0.5)
        self.finisher_attack_sound = pygame.mixer.Sound("files/audio/finisher.wav")
        self.finisher_attack_sound.set_volume(0.5)
        self.blocked_attack_sound = pygame.mixer.Sound("files/audio/blockedatk.wav")
        self.blocked_attack_sound.set_volume(0.5)
        self.parried_attack_sound = pygame.mixer.Sound("files/audio/parriedatk.wav")
        self.parried_attack_sound.set_volume(0.5)
        self.death_effect_sound = pygame.mixer.Sound("files/audio/death.wav")
        self.death_effect_sound.set_volume(0.5)

        

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

    def move(self, width, height, surface, target, events):
        SPEED = 7
        GRAVITY = 3
        dx = 0
        dy = 0
        self.moving = False
        self.blocking = False
        self.attack_type = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # Handle events specific to this fighter
        for event in events:  # Pass the event list to this method
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code(self.block):
                    if not self.parry_window:  # Only activate parry if it's not already active
                        self.parry_window = True
                        self.parry_timer = pygame.time.get_ticks()  # Start the parry timer
                        print(f"Parry window activated for fighter at {self.rect.topleft}")

        # Check if the parry window has expired
        if self.parry_window and pygame.time.get_ticks() - self.parry_timer > self.parry_duration:
            self.parry_window = False
            print(f"Parry window expired for fighter at {self.rect.topleft}")
            print(self.parry_window)
        if not self.attacking and not self.hit:
            if key[pygame.key.key_code(self.block)]:
                self.blocking = True

            # Movement key presses
            if key[pygame.key.key_code(self.left)]:
                dx = -SPEED
                self.moving = True
            if key[pygame.key.key_code(self.right)]:
                dx = SPEED
                self.moving = True
            if key[pygame.key.key_code(self.up)] and not self.jump:
                self.vel_y = -30
                self.jump = True
                self.moving = False

            # Attacking keys
            if not self.jump:
                if key[pygame.key.key_code(self.attack1)]:
                    self.attack_type = 1
                    self.light_attack_sound.play()
                    self.attack(surface, target)
                if key[pygame.key.key_code(self.attack2)]:
                    self.attack_type = 2
                    self.medium_attack_sound.play()
                    self.attack(surface, target)
                if key[pygame.key.key_code(self.attack3)]:
                    self.attack_type = 3
                    self.heavy_attack_sound.play()
                    self.attack(surface, target)

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Check screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > width:
            dx = width - self.rect.right
        if self.rect.bottom + dy > height - 60:
            self.vel_y = 0
            self.jump = False
            dy = height - 60 - self.rect.bottom

        # Check if players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def frame_handler(self):
        #new method ensures that i restart the next action from the start of the frame index, stopping the index out of range error. 
        #must make sure that jump is before moving, otherwise when I jump it causes problems
        if self.health <= 0:
            self.alive = False
            self.action_handler(6)#death
        elif self.hit == True:
            self.action_handler(5)#hitstun
        elif self.jump == True:
            self.action_handler(7)#jump
        elif self.attacking == True:
            if self.attack_type == 1:
                self.action_handler(2)#lattack
            elif self.attack_type == 2:   
                self.action_handler(3)#mattack
            elif self.attack_type == 3:
                self.action_handler(4)#hattack
        
        elif self.moving == True:
            self.action_handler(1)#walk
        elif self.blocking == True:
            self.action_handler(8)
        else:
            self.action_handler(0)#idle
    
        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 150
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                #check to see if player is dead
                if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) -1
                else:
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
    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width + 100, self.rect.height)
            if attack_hitbox.colliderect(target.rect):
                if not target.blocking and not target.parry_window:
                    target.damage(10)
                    self.finisher_meter(10)
                    target.hit = True
                    print("hit")
                    print(target.health)

                # Ensure parry only happens when parry_window is active and target is not blocking
                elif target.parry_window:
                    target.finisher_meter(20)
                    print("parried")
                    self.parried_attack_sound.play()
                    self.hit = True
                    self.attack_cooldown = 30
                    if self.flip == False: 
                        parry_effect_x = target.rect.centerx
                    else:
                        parry_effect_x = target.rect.centerx  - 70
                    parry_effect_y = target.rect.top - 60
                    surface.blit(self.parry_effect, (parry_effect_x, parry_effect_y))

                elif target.blocking:
                    print("blocked")
                    self.blocked_attack_sound.play()
                    # Adjust block effect position to align with the side of the target's rect
                    if self.flip == False: 
                        block_effect_x = target.rect.left - 50
                    else:
                        block_effect_x = target.rect.right - 50  
    #                block_effect_y = target.rect.top - 70
     #               surface.blit(self.block_effect, (block_effect_x, block_effect_y))
                    # Fix animations bugging
                    if self.attack_type == 1:
                        self.action_handler(2)
                    elif self.attack_type == 2:
                        self.action_handler(3)
                    else:
                        self.action_handler(4)

        # pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt):
        self.health -= damage_dealt
        if self.health <= 0:
            self.action_handler(6)

    def draw(self, surface):
        # Create a separate flipped image (img) so that players face each other if they pass
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255,255,255), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

        # Render the parry box only if the parry window is active for this fighter
        if self.parry_window:
            if self.flip:
                parry_x = self.rect.x - 100
            else:
                parry_x = self.rect.x + 100
            parry_y = self.rect.y - 50
            parry_rect = pygame.Rect(parry_x, parry_y, 20, 180)
            pygame.draw.rect(surface, (255, 0, 0), parry_rect)  # Draw the parry box




