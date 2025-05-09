import pygame
import csv  # Import csv module
from pygame import mixer
mixer.init()

#errors i encountered x = didnt fix v = did! 
#v - when i attack whilst moving, become trapped in walking animation
#v - can move whilst hit
#v - interrupting attacks with an attack wouldnt play hit animation
#v - finisher meter goes to wrong person
#v - hit animation goes to other person
#v - hit animation would break other animations
#v - attacking a blocking fighter sometimes locks person who attacks the blocking fighter into walking animation
#v - parry window is not working - attacks cannot be parried
#x - takes no damage if moving whilst blocking - should stop blocking but doesnt ):
#x - hitstun goes to other person when parrying
#x - blocking is not broke by finishers
#x - damage the same for all classes


#to do
 #each attack has different damages - three types of attack - damage will vary depending of character class
# v/x - light attack - will be a light jab with little knockback and closer range - good for starting combos
# v/x - medium attack - will be a punch with some knockback - slightly larger range so connecting will be easier
# v/x - heavy attack - will be an attack with a lot of knockback - large range but slower to execute
# x/x - finisher - will be a powerful attack that can only be used when the finisher meter is full 
# v - parry - will be a defensive move that can be used if you block an attack quickly, will grant significant finisher meter if you know the timing
# v - blocking - will be a defensive move that negates damage taken from attacks, can be broken by heavy attacks
# v - hitstun timer - when hit, will be stunned for a set amount of time

try:
    with open("selected_characters.txt", "r") as file:
        p1_selected = file.readline().strip()
        p2_selected = file.readline().strip()
except FileNotFoundError:
    print("Error: Selected characters file not found.")
    p1_selected = None
    p2_selected = None

print(f"Player 1 selected: {p1_selected}")
print(f"Player 2 selected: {p2_selected}")

# Load settings from CSV
def load_settings():
    settings = {"music_on": True, "sound_effects_on": True}
    try:
        with open("settings.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "music":
                    settings["music_on"] = row[1].strip().lower() == "on"
                elif row[0] == "sfx":
                    settings["sound_effects_on"] = row[1].strip().lower() == "on"
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
    return settings

# Load settings and set volumes
settings = load_settings()
music_volume = 0.5 if settings["music_on"] else 0
sfx_volume = 0.5 if settings["sound_effects_on"] else 0

pygame.mixer.music.set_volume(music_volume)
print(f"Music volume: {music_volume}")
print(f"Sound effects volume: {sfx_volume}")

class Fighter():
    def __init__(self,x,y,input_left,input_right,input_up,attack1,attack2,attack3,block,health, data, sprite_sheet, animation_steps):
        self.finisher_status = False
        self.parry_window = False #parry window is the period of time in which you are able to parry
        self.parry_timer = 0 #measures how long the parry has been going
        self.parry_duration = 300 #the maximum time the parry can go
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
        self.vel_x = 0 #velocity on x
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
        self.winner = None  # Attribute to track the winner
        #load audio
        pygame.mixer.music.load("files/audio/background_music.mp3")
        pygame.mixer.music.set_volume(music_volume)  # Set initial volume based on settings
        pygame.mixer.music.play(-1)  #loop infinitely
        self.light_attack_sound = pygame.mixer.Sound("files/audio/lighthit.wav") #load all sound effects
        self.light_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.medium_attack_sound = pygame.mixer.Sound("files/audio/mediumhit.wav")
        self.medium_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.heavy_attack_sound = pygame.mixer.Sound("files/audio/heavyhit.wav")
        self.heavy_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.finisher_attack_sound = pygame.mixer.Sound("files/audio/finisher.wav")
        self.finisher_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.blocked_attack_sound = pygame.mixer.Sound("files/audio/blockedatk.wav")
        self.blocked_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.parried_attack_sound = pygame.mixer.Sound("files/audio/parriedatk.wav")
        self.parried_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.missed_attack_sound = pygame.mixer.Sound("files/audio/missedatk.wav")
        self.missed_attack_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.death_effect_sound = pygame.mixer.Sound("files/audio/death.wav")
        self.death_effect_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.lfighterfinisher_sound = pygame.mixer.Sound("files/audio/lfighterfinisher.wav")
        self.lfighterfinisher_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.mfighterfinisher_sound = pygame.mixer.Sound("files/audio/mfighterfinisher.wav")
        self.mfighterfinisher_sound.set_volume(sfx_volume)  # Set initial volume based on settings
        self.hfighterfinisher_sound = pygame.mixer.Sound("files/audio/hfighterfinisher.wav")
        self.hfighterfinisher_sound.set_volume(sfx_volume)  # Set initial volume based on settings
  
        
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
        if self.vel_x != 0:
            self.rect.x += self.vel_x
            if self.vel_x>0:
                self.vel_x-=1
            if self.vel_x<0:
                self.vel_x+=1
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
        #order priority - death, hit, jump, attack, walk, idle
        if self.health <= 0:
            self.alive = False
            self.action_handler(6)  # death
        elif self.hit:
            self.action_handler(5)  # hit
        elif self.jump:
            self.action_handler(7)  # jump
        elif self.attacking:
            if self.attack_type == 1:
                self.action_handler(2)  # l_attack
            elif self.attack_type == 2:
                self.action_handler(3)  # m_attack
            elif self.attack_type == 3:
                self.action_handler(4)  # h_attack
            elif self.attack_type == 4:
                self.action_handler(9)  # finisher
                self.finisher_status = False
        elif self.moving:
            self.action_handler(1)  # walk
        elif self.blocking and not self.moving:
            self.action_handler(8)  # block
        else:
            self.action_handler(0)  # idle

        self.image = self.animation_list[self.action][self.frame_index]
        animation_cooldown = 150
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):  # End of animation
                if not self.alive:
                    self.frame_index = len(self.animation_list[self.action]) - 1  # Last frame of death animation
                else:
                    self.frame_index = 0  # Reset frame index
                    if self.action in [2, 3, 4, 9]:
                        self.attacking = False  # Reset attacking after attack animation

                        # Define cooldown values for each class
                        cooldown_values = {
                            "light": 10,
                            "medium": 15,
                            "heavy": 20
                        }

                        # Set attack cooldown based on player class
                        if p1_selected in cooldown_values and p2_selected in cooldown_values:
                            if p1_selected != p2_selected:
                                self.attack_cooldown = cooldown_values[p1_selected]

                        # Reset finisher value after use
                        if self.finisher_status:
                            self.finisher_value = 0

                    if self.hit:
                        # Interrupt attack if hit during wind-up
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
            attack_hitbox = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width + 100,
                self.rect.height
            )
            
            # Define damage and knockback values for each class
            attack_values = {
                "light": {"damage": [5, 10, 15], "knockback": [3, 6, 9]},
                "medium": {"damage": [7, 15, 20], "knockback": [5, 8, 12]},
                "heavy": {"damage": [10, 20, 30], "knockback": [7, 10, 15]},
            }

            # Assign player classes based on the selected characters
            p1_character = p1_selected  # Player 1's selected character class
            p2_character = p2_selected  # Player 2's selected character class

            # Check attack hit
            if attack_hitbox.colliderect(target.rect):
                # If the target is not blocking or parrying
                if not target.blocking and not target.parry_window:
                    if self.attack_type in [1, 2, 3]:  # Light, Medium, Heavy attacks
                        damage = attack_values[p1_character]["damage"][self.attack_type - 1]
                        knockback = attack_values[p1_character]["knockback"][self.attack_type - 1]
                        target.damage(damage, target, knockback)
                        target.hitstun(100 * self.attack_type)
                        self.finisher_meter(10 * self.attack_type)
                        if self.attack_type == 1:
                            self.light_attack_sound.play()
                        elif self.attack_type == 2:
                            self.medium_attack_sound.play()
                        elif self.attack_type == 3:
                            self.heavy_attack_sound.play()
                    elif self.attack_type == 4:  # Finisher
                        self.mfighterfinisher_sound.play()
                        if self.finisher_status:
                            target.hitstun(1000)
                            target.damage(50, target, 20)
                            self.finisher_value = 0  # Reset finisher meter

                # Parry logic - if the target is in a parry window
                elif target.parry_window:
                    target.finisher_meter(200)
                    print("parried")
                    self.parried_attack_sound.play()
                    self.hitstun(500)
                    self.attack_cooldown = 30
                    parry_effect_x = self.rect.centerx - 100
                    parry_effect_y = self.rect.top - 60
                    surface.blit(self.parry_effect, (parry_effect_x, parry_effect_y))

                # Blocking logic - if the target is blocking
                elif target.blocking:
                    # Heavy class attacks can break blocking
                    if p1_character == "heavy":
                        target.damage(20, target, 10)
                        target.hitstun(1000)
                        target.hit = True
                        self.finisher_meter(20)
                        self.heavy_attack_sound.play()
                    else:
                        print("blocked")
                        self.blocked_attack_sound.play()
            else:
                self.missed_attack_sound.play()

    def damage(self, damage_dealt, target, knockback):
        self.health -= damage_dealt
        if self.flip:
            target.vel_x = abs(knockback)
        else:
            target.vel_x = -abs(knockback)
        if self.health <= 0:
            self.winner = "Player 2"
        if target.health <= 0:
            target.winner = "Player 1"
    def hitstun(self,hitstun_duration):
        self.hit = True
        print(self.hitstun_start)
    #    print(f"target.hit = {target.hit}")
        self.hitstun_start = pygame.time.get_ticks()
        
        self.hitstun_duration = hitstun_duration
      #  print(f"Hitstun duration: {self.hitstun_duration} and current time: {pygame.time.get_ticks()}")




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