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
#x - hitstun goes to other person when parrying


#to do
 #each attack has different damages - three types of attack - damage will vary depending of character class
# v/x - light attack - will be a light jab with little knockback and closer range - good for starting combos
# v/x - medium attack - will be a punch with some knockback - slightly larger range so connecting will be easier
# v/x - heavy attack - will be an attack with a lot of knockback - large range but slower to execute
# x/x - finisher - will be a powerful attack that can only be used when the finisher meter is full 
# v - parry - will be a defensive move that can be used if you block an attack quickly, will grant significant finisher meter if you know the timing
# v - blocking - will be a defensive move that negates damage taken from attacks, can be broken by heavy attacks
# x - hitstun timer - when hit, will be stunned for a set amount of time

class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3,block,health, data, sprite_sheet, animation_steps):
        self.finisher_status = False
        self.parry_window = False #parry window is the period of time in which you are able to parry
        self.parry_timer = 0 #measures how long the parry has been going
        self.parry_duration = 00 #the maximum time the parry can go
        self.hitstun_start = 0 #the time the player is stunned for when hit
        self.hitstun_duration = 0 #the duration of the hitstun
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

        #pygame.mixer.music.play(-1)  #loop infinitely
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
        self.missed_attack_sound = pygame.mixer.Sound("files/audio/missedatk.wav")
        self.missed_attack_sound.set_volume(0.5)
        self.death_effect_sound = pygame.mixer.Sound("files/audio/death.wav")
        self.death_effect_sound.set_volume(0.5)
        self.lfighterfinisher_sound = pygame.mixer.Sound("files/audio/lfighterfinisher.wav")
        self.lfighterfinisher_sound.set_volume(0.5)
        self.mfighterfinisher_sound = pygame.mixer.Sound("files/audio/mfighterfinisher.wav")
        self.mfighterfinisher_sound.set_volume(0.5)
        self.hfighterfinisher_sound = pygame.mixer.Sound("files/audio/hfighterfinisher.wav")
        self.hfighterfinisher_sound.set_volume(0.5)
  
        
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

        
        if target.hit and pygame.time.get_ticks() - target.hitstun_start > target.hitstun_duration:
            target.hit = False
            target.hitstun_duration = 0
            target.action_handler(0)
            print("Hitstun ended, target.hit set to False")
            
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
                    if self.finisher_value >= 200:
                        self.attack_type = 4
                        self.finisher_status = True
                    else:   
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
        #order priority - death, hit, jump, attack, block, walk, idle
        if self.health <= 0:
            self.alive = False
            self.action_handler(6)  # death
        elif self.hit == True:
            self.action_handler(5)  # hit
        elif self.jump == True:
            self.action_handler(7)  # jump
        elif self.blocking == True:
            self.action_handler(8)  # block
        elif self.attacking == True:
            if self.attack_type == 1:
                self.action_handler(2)  # lattack
            elif self.attack_type == 2:
                self.action_handler(3)  # mattack
            elif self.attack_type == 3:
                self.action_handler(4)  # hattack
            elif self.attack_type == 4:
                self.action_handler(9)  # finisher
                self.finisher_status = False
        
        elif self.moving == True:
            self.action_handler(1)  # walk
        else:
            self.action_handler(0)  # idle

        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 150
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):  # if the frame index is at the end of the current animation
                if self.alive == False:
                    self.frame_index = 0
                else:
                    self.frame_index = 0  # reset the frame index
                    if self.action in [2, 3, 4, 9]:
                        self.attacking = False  # only reset attacking when the attack is done
                        self.attack_cooldown = 10
                    if self.hit == True:
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
        if self.finisher_value >= 200:
            self.finisher_attack_sound.play()
    
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
                        target.hitstun(target,100)
                        self.finisher_meter(10)
                        self.light_attack_sound.play()

                    elif self.attack_type == 2:
                        target.damage(6,target)
                        target.hitstun(target,300)
                        self.finisher_meter(15)
                        self.medium_attack_sound.play()
                    
                    elif self.attack_type == 3:
                        target.damage(10,target)
                        target.hitstun(target,700)
                        self.heavy_attack_sound.play()
                        self.finisher_meter(20)

                    elif self.attack_type == 4:
                        self.mfighterfinisher_sound.play()
                        if self.finisher_status == True:
                            for i in range(0,5):
                                target.hitstun(target,1000)
                                target.damage(10,target)
                                self.finisher_meter(-200)

                #parry logic - parrying only happens when parry_window is True 
                elif target.parry_window:
                    target.finisher_meter(200)
                    print("parried")
                    self.parried_attack_sound.play()
                    
                    target.hitstun(target,500)
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
                        target.hitstun(target,1000)
                        target.hit = True
                        self.finisher_meter(20)
                        self.finisher_attack_sound.play()
                    else:    
                        print("blocked")
                        self.blocked_attack_sound.play()
            else:
                self.missed_attack_sound.play()



         ##           # Fix animations bugging
           #         if self.attack_type == 1:
            #            self.action_handler(2)
             #       elif self.attack_type == 2:
              #          self.action_handler(3)
               #     else:
                #        self.action_handler(4)

        #pygame.draw.rect(surface, (0,255,0), attack_hitbox)

    def damage(self,damage_dealt,target):
        self.health -= damage_dealt
        if target.health <= 0:
            target.death_effect_sound.play()

    def hitstun(self,target,hitstun_duration):
        target.hit = True
        print(target.hitstun_start)
        print(f"target.hit = {target.hit}")
        target.hitstun_start = pygame.time.get_ticks()
        
        target.hitstun_duration = hitstun_duration
        print(f"Hitstun duration: {target.hitstun_duration} and current time: {pygame.time.get_ticks()}")




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

#errors
#x - can still type more than 2 chars
#v - letters vanished moment they appeared - pass input_text as param
#v - not going to new line in csv file 



import pygame

from pygame import mixer
import csv

mixer.init()
pygame.init()

#create game window
res = 1000,600
screen = pygame.display.set_mode((res))
pygame.display.set_caption("Fighting game")



smallfont = pygame.font.Font('files/mini_pixel-7.ttf',100)
errorfont = pygame.font.Font('files/Game Paused DEMO.ttf',50)
gameoverfont = pygame.font.Font('files/mini_pixel-7.ttf',150)
winscreenfont = pygame.font.Font('files/mini_pixel-7.ttf',125)
colour_dark = (100, 100, 100)
colour_light = (170, 170, 170)
input_box = pygame.Rect(200,200,150, 100)
input_text = ""  # The text the user types
input_active = False 
#define fighter variables
FIGHTER_SIZE = 200

#the scale for each sprite
FIGHTER_SCALE = 4

#manual offset so that the sprite is within the hitbox
LIGHT_FIGHTER_OFFSET = [90,83]
MEDIUM_FIGHTER_OFFSET = [90,83]
HEAVY_FIGHTER_OFFSET = [80,80]

MEDIUM_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, MEDIUM_FIGHTER_OFFSET]
HEAVY_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, HEAVY_FIGHTER_OFFSET]
LIGHT_FIGHTER_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, LIGHT_FIGHTER_OFFSET]
#create background image
bg_image= pygame.image.load("files/assets/background.png").convert_alpha()

#load spritesheet
light_fighter_sheet = pygame.image.load("files/assets/Light Fighter Spritesheet.png").convert_alpha()
medium_fighter_sheet = pygame.image.load("files/assets/Normal Fighter Spritesheet.png").convert_alpha()
heavy_fighter_sheet = pygame.image.load("files/assets/Heavy Fighter Spritesheet.png").convert_alpha()
#number of steps for each animation
light_animation_steps = [4,5,2,2,3,1,5,3,1,6]
medium_animation_steps  = [4,6,2,3,3,1,5,3,1,4]
heavy_animation_steps =   [4,4,3,3,3,1,4,3,1,6]
#set framerate
clock = pygame.time.Clock()



def draw_bg():
    width = screen.get_width()
    height = screen.get_height()
    scaled_bg = pygame.transform.scale(bg_image, (width, height))
    screen.blit(scaled_bg, (0, 0))

#function for drawing healthbar
def draw_healthbar(health, x,y):
    health_ratio = health/100
    pygame.draw.rect(screen, (139,0,0), (x-3,y-3,406,36))
    pygame.draw.rect(screen, (139,0,0), (x,y,400,30))
    pygame.draw.rect(screen, (255,0,0), (x,y,400*health_ratio,30))
def draw_finisherbar(finisher_value, x, y):
    pygame.draw.rect(screen,(colour_dark), (x-3,y-3,206,26))
    pygame.draw.rect(screen,(26, 43, 68), (x,y,200,20))
    pygame.draw.rect(screen, (59, 130, 246), (x,y,0+finisher_value,20))

width = screen.get_width()
height = screen.get_height()

#instantiate fighters

fighter_1 = Fighter(200,350,"a","d","w","x","c","v","f",100,MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)
fighter_2 = Fighter(700,350,"LEFT","RIGHT","UP","B","N","M","l",100,MEDIUM_FIGHTER_DATA, medium_fighter_sheet, medium_animation_steps)


#game loop
run = True
while run:
    clock.tick(60)

    # Retrieve all events once per frame
    events = pygame.event.get()

    #draw background
    draw_bg()
    
    #show player health
    draw_healthbar(fighter_1.health, 20, 20)
    draw_healthbar(fighter_2.health, 580, 20)
   
    #draw player finisher
    draw_finisherbar(fighter_1.finisher_value, 20, 60)
    draw_finisherbar(fighter_2.finisher_value, 780, 60)

    #frame handling
    fighter_1.frame_handler()
    fighter_2.frame_handler()

    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #move fighters
    fighter_1.move(width, height, screen, fighter_2, events)
    fighter_2.move(width, height, screen, fighter_1, events)

    #event handler
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()
