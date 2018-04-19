import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    
    def __init__(self, ai_settings, screen):
        
        super(Ship, self).__init__()
        #initial ship and its starting position
        self.screen = screen
        self.ai_settings = ai_settings
        #load image of ship
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
    
        #put every ship in the middle of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        
        #moving signal
        self.moving_right = False
        self.moving_left = False    
                
    def update(self):
        #adjust the position of ship based on moving signal
        #update center of ship, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        #update rect based on self.center
        self.rect.centerx = self.center
            
    
    def blitme(self):
        #draw ship in sepcific position
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        #put ship in the middle of screen
        self.center = self.screen_rect.centerx
        
        
        
        
