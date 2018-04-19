import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    #create alien class
    
    def __init__(self, ai_settings, screen):
        #initial alien and set its position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load alien image, set rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #each alien appears in top left at first
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store position of alien
        self.x = float(self.rect.x)
        
    def blitme(self):
        #draw alien in sepecific position
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        #alien move left or right
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def check_edges(self):
        #if at edge, return true
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True