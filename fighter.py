import pygame

#errors i encountered x = didnt fix v = did! 
#v - when i attack whilst moving, become trapped in walking animation
#v/x - can move whilst hit
#v - interrupting attacks with an attack wouldnt play hit animation
#v - finisher meter goes to wrong person
#v - hit animation goes to other person
#v - hit animation would break other animations
#v - attacking a blocking fighter sometimes locks person who attacks the blocking fighter into walking animation
#v - parry window is not working - attacks cannot be parried
#x - takes no damage if moving whilst blocking - should stop blocking but doesnt ):


#to do
 #each attack has different damages - three types of attack - damage will vary depending of character class
# v/x - light attack - will be a light jab with little knockback and closer range - good for starting combos
# v/x - medium attack - will be a punch with some knockback - slightly larger range so connecting will be easier
# v/x - heavy attack - will be an attack with a lot of knockback - large range but slower to execute
# x/x - finisher - will be a powerful attack that can only be used when the finisher meter is full 
# v - parry - will be a defensive move that can be used if you block an attack quickly, will grant significant finisher meter if you know the timing
# v - blocking - will be a defensive move that negates damage taken from attacks, can be broken by heavy attacks


class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3,block,health, data, sprite_sheet, animation_steps):
        self.parry_window = False #parry window is the period of time in which you are able to parry
        self.parry_timer = 0 #measures how long the parry has been going
        self.parry_duration = 300 #the maximum time the parry can go
        self.size = data[0] #the size of the sprite - taken from the data list which is passed in as a parameter to take FIGHTER_DATA
        self.image_scale = data[1]#the same as above but for the scale of the spriter
        self.offset = data[2] #the offset of the sprite to ensure it is centered to the player rect
        self.rect = pygame.Rect((x,y,80,180)) #the player rect
        self.block_effect = pygame.image.load("files/assets/dustcloud.png").convert_alpha() #load the block effect
        self.block_effect = pygame.transform.scale(self.block_effect, (100, 100)) #scale the block effect
        self.parry_effect = pygame.image.load("files/assets/parry_icon.png").convert_alpha() #load the parry effect
        self.parry_effect = pygame.transform.scale(self.parry_effect, (200, 200))  #scale the parry effect 
        self.vel_y = 0 #velocity on y 
        self.jump = False #check if jumping
        self.moving = False #check if moving
        self.blocking = False #check if blocking
        self.left = input_left #move left input
        self.right = input_right #move right input
        self.up = input_up #jump input
        self.health = health #player health
        self.finisher_value = 0 #starting finisher value
        self.animation_list = self.load_images(sprite_sheet, animation_steps) #load the images from the spritesheet
        self.action = 0#0: idle, 1: walk, 2: l_attack, 3: m_attack, 4: h_attack, 5: hit,6:death, 7: jump, 8: block
        self.update_time= pygame.time.get_ticks() #update time
        self.frame_index = 0 #frame index always starts at 0 - the first frame of the animation cycle
        self.image = self.animation_list[self.action][self.frame_index] #the image is saved as both the action and the frame
        self.attack1 = attack1 #attack 1 input
        self.attack2 = attack2 #attack 2 input
        self.attack3 = attack3 #attack 3 input
        self.block = block #block input
        self.attack_type = 0 #check the attack type
        self.flip = False #if the player is flipped
        self.attacking = False #if the player is attacking
        self.attack_cooldown = 0 #cooldown between attakcs
        self.hit = False #if the player is hit
        self.alive = True #if the player is alive
        #load audio
        pygame.mixer.music.load("files/audio/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  #loop infinitely
        self.light_attack_sound = pygame.mixer.Sound("files/audio/lighthit.wav") #load all sound effects
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
        self.selection  = pygame.mixer.Sound("files/audio/selection.wav")
        self.invalidselection = pygame.mixer.Sound("files/audio/invalidselection.wav")
        
#extract the images from the spritesheet for the current character selected
    def load_images(self,sprite_sheet, animation_steps):
        animation_list = [] #create a list to store the animations
        for y, animation in enumerate(animation_steps): #iterate over each row of the spritesheet, y being the row index with animation being the number of frames
            temp_img_list = [] #temportary list to store current rows frames
            for x in range(animation): #loops through each frame of current row
                temp_img = sprite_sheet.subsurface(x * self.size, y*self.size, self.size, self.size) #extracts the frame (subsurface) which is determined by the row (y) and the column (x), with the subsurface size bieng self.size
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))) #rescales extracted frame and adds it to the temp image list
            animation_list.append(temp_img_list) #adds the whole list of frames to the main animation
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
            
        #handle blocking
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
                  #  self.light_attack_sound.play()
                    self.attack(surface, target)
                if key[pygame.key.key_code(self.attack2)]:
                    self.attack_type = 2
                  #  self.medium_attack_sound.play()
                    self.attack(surface, target)
                if key[pygame.key.key_code(self.attack3)]:
                    self.attack_type = 3
                  #  self.heavy_attack_sound.play()
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
        #order priority - death, hit, jump, attack, walk, idle - if order is changed causes errors like can attack while jumping or unable to walk + attack at once
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
        elif self.blocking == True and not self.moving:
            self.action_handler(8)
        else:
            self.action_handler(0)#idle
    
        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 150
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):  #if the frame index is at the end of the current animation
                #check to see if player is dead
                if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) -1 #set the frame index to the last frame of the death animation
                else:
                    self.frame_index = 0  #reset the frame index
                    if self.action in [2,3,4]:
                        self.attacking = False  #only have self.attacking reset to false when the attack is done
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
            
            #check attack hit 
            if attack_hitbox.colliderect(target.rect):
                #attack logic - can only be damaged when not blocking or parrying
                if not target.blocking and not target.parry_window:
                    if self.attack_type == 1:
                        target.damage(2,target)
                        self.finisher_meter(10)
                        self.light_attack_sound.play()

                    elif self.attack_type == 2:
                        target.damage(6,target)
                        self.finisher_meter(15)
                        self.medium_attack_sound.play()
                    
                    elif self.attack_type == 3:
                        target.damage(10,target)
                        self.heavy_attack_sound.play()
                        self.finisher_meter(20)

                #parry logic - parrying only happens when parry_window is True 
                elif target.parry_window:
                    target.finisher_meter(20)
                    print("parried")
                    self.parried_attack_sound.play()
                    self.hit = True
                    self.attack_cooldown = 30
                    if self.flip == False: 
                        parry_effect_x = self.rect.centerx - 100
                    else:
                        parry_effect_x = self.rect.centerx - 100
                    parry_effect_y = self.rect.top - 60
                    surface.blit(self.parry_effect, (parry_effect_x, parry_effect_y))
                
                #blocking logic - damage only negated if blocking
                elif target.blocking:
                    #blocking can be broke by heavy attack
                    if self.attack_type == 3:
                        target.damage(20,target)
                        target.hit = True
                        self.finisher_meter(20)
                        self.finisher_attack_sound.play()
                    else:    
                        print("blocked")
                        self.blocked_attack_sound.play()

         ##           # Fix animations bugging
           #         if self.attack_type == 1:
            #            self.action_handler(2)
             #       elif self.attack_type == 2:
              #          self.action_handler(3)
               #     else:
                #        self.action_handler(4)

        # pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt,target):
        self.health -= damage_dealt
        target.hit = True
        print("hit")
        print(target.health)
        if target.health <= 0:
            target.death_effect_sound.play()

    def draw(self, surface):
        # Create a separate flipped image (flipped_img) so that players face each other if they pass
        flipped_img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255,255,255), self.rect)
        surface.blit(flipped_img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

        # Render the parry box only if the parry window is active for this fighter
        if self.parry_window:
            if self.flip:
                parry_x = self.rect.x - 100
            else:
                parry_x = self.rect.x + 100
            parry_y = self.rect.y - 50
            parry_rect = pygame.Rect(parry_x, parry_y, 20, 180)
            #pygame.draw.rect(surface, (255, 0, 0), parry_rect)  # Draw the parry box