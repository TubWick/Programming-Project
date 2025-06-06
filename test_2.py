import pygame
pygame.init()

# Initialize screen and clock
screen = pygame.display.set_mode((1280, 620))
clock = pygame.time.Clock()

smallfont = pygame.font.Font('files/mini_pixel-7.ttf', 50)
shenttpuro = pygame.font.Font('files/Shenttpuro Font.ttf', 100)
text_surf = shenttpuro.render('First Strike', True, (255, 10, 10))


class Charselectionscreen():
    def __init__(self, x, y):
        try:
            self.lighticon = pygame.image.load("files/assets/lighticon.png").convert_alpha()
            self.mediumicon = pygame.image.load("files/assets/mediumicon.png").convert_alpha()
            self.heavyicon = pygame.image.load("files/assets/heavyicon.png").convert_alpha()
            self.p1marker = pygame.image.load("files/assets/p1marker.png").convert_alpha()
            self.p2marker = pygame.image.load("files/assets/p2marker.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            pygame.quit()
            exit()
        self.x = x
        self.y = y
        self.lighticon = pygame.transform.scale(self.lighticon, (400, 450))
        self.mediumicon = pygame.transform.scale(self.mediumicon, (400, 450))
        self.heavyicon = pygame.transform.scale(self.heavyicon, (400, 450))
        self.p1marker = pygame.transform.scale(self.p1marker, (150, 150))
        self.p2marker = pygame.transform.scale(self.p2marker, (150, 150))
        self.l_mask = pygame.mask.from_surface(self.lighticon)
        self.l_outline = self.l_mask.outline()
        self.m_mask = pygame.mask.from_surface(self.mediumicon)
        self.m_outline = self.m_mask.outline()
        self.h_mask = pygame.mask.from_surface(self.heavyicon)
        self.h_outline = self.h_mask.outline()
        self.l_rect = self.lighticon.get_rect(topleft=(self.x - 480, self.y - 150))
        self.m_rect = self.mediumicon.get_rect(topleft=(self.x - 50, self.y - 150))
        self.h_rect = self.heavyicon.get_rect(topleft=(self.x + 370, self.y - 150))
        self.hovercolour = (255, 255, 255)
        self.selectedcolour = (255, 10, 10)
        self.l_offset_outline = [(p[0] + self.l_rect.x, p[1] + self.l_rect.y) for p in self.l_outline]
        self.m_offset_outline = [(p[0] + self.m_rect.x, p[1] + self.m_rect.y) for p in self.m_outline]
        self.h_offset_outline = [(p[0] + self.h_rect.x, p[1] + self.h_rect.y) for p in self.h_outline]
        self.p1_selected = None  
        self.p2_selected = None  
        self.turn = "p1"  
        self.mouse_pressed = False  # Track mouse button state

    def draw_cs_screen(self):
        #blitting icons
        screen.blit(self.lighticon, (self.x - 480, self.y - 150))
        screen.blit(self.mediumicon, (self.x - 50, self.y - 150))
        screen.blit(self.heavyicon, (self.x + 370, self.y - 150))
        #blitting descriptions
        l_desc_surf = smallfont.render('Light Fighter', True, (255, 255, 255))
        screen.blit(l_desc_surf, (self.x - 400, self.y + 300))
        m_desc_surf = smallfont.render('Medium Fighter', True, (255, 255, 255))
        screen.blit(m_desc_surf, (self.x + 25, self.y + 300))
        h_desc_surf = smallfont.render('Heavy Fighter', True, (255, 255, 255))
        screen.blit(h_desc_surf, (self.x + 470, self.y + 300))

    def ifhover(self):
        if self.l_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.polygon(screen, (self.hovercolour), self.l_offset_outline, 10)
        if self.m_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.polygon(screen, (self.hovercolour), self.m_offset_outline, 10)
        if self.h_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.polygon(screen, (self.hovercolour), self.h_offset_outline, 10)

    def ifclicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.mouse_pressed:
            self.mouse_pressed = True  # Set flag when button is pressed
            if self.turn == "p1":  # Player 1 selection
                if self.l_rect.collidepoint(pygame.mouse.get_pos()) and self.p2_selected != "light":
                    self.p1_selected = "light"
                elif self.m_rect.collidepoint(pygame.mouse.get_pos()) and self.p2_selected != "medium":
                    self.p1_selected = "medium"
                elif self.h_rect.collidepoint(pygame.mouse.get_pos()) and self.p2_selected != "heavy":
                    self.p1_selected = "heavy"
                if self.p1_selected:  # Switch turn only after valid selection
                    self.turn = "p2"
            elif self.turn == "p2":  # Player 2 selection
                if self.l_rect.collidepoint(pygame.mouse.get_pos()) and self.p1_selected != "light":
                    self.p2_selected = "light"
                elif self.m_rect.collidepoint(pygame.mouse.get_pos()) and self.p1_selected != "medium":
                    self.p2_selected = "medium"
                elif self.h_rect.collidepoint(pygame.mouse.get_pos()) and self.p1_selected != "heavy":
                    self.p2_selected = "heavy"
                if self.p2_selected:  # Switch turn only after valid selection
                    self.turn = "p1"
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_pressed = False  # Reset flag when button is released

    def draw_selected_outline(self):
        # Draw outlines and markers for p1
        if self.p1_selected == "light":
            pygame.draw.polygon(screen, (self.selectedcolour), self.l_offset_outline, 10)
            screen.blit(self.p1marker, self.l_rect.topleft)
        elif self.p1_selected == "medium":
            pygame.draw.polygon(screen, (self.selectedcolour), self.m_offset_outline, 10)
            screen.blit(self.p1marker, self.m_rect.topleft)
        elif self.p1_selected == "heavy":
            pygame.draw.polygon(screen, (self.selectedcolour), self.h_offset_outline, 10)
            screen.blit(self.p1marker, self.h_rect.topleft)

        # Draw outlines and markers for p2
        if self.p2_selected == "light":
            pygame.draw.polygon(screen, (self.selectedcolour), self.l_offset_outline, 10)
            screen.blit(self.p2marker, self.l_rect.topleft)
        elif self.p2_selected == "medium":
            pygame.draw.polygon(screen, (self.selectedcolour), self.m_offset_outline, 10)
            screen.blit(self.p2marker, self.m_rect.topleft)
        elif self.p2_selected == "heavy":
            pygame.draw.polygon(screen, (self.selectedcolour), self.h_offset_outline, 10)
            screen.blit(self.p2marker, self.h_rect.topleft)

characterselection = Charselectionscreen(500, 200)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))
    characterselection.ifhover()
    characterselection.draw_cs_screen()
    characterselection.ifclicked(event)
    characterselection.draw_selected_outline()

    pygame.display.update()
    clock.tick(60)  # Limit frame rate