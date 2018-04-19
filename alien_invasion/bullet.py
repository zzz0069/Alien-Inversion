import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        #create a bullet object
        super(Bullet, self).__init__()
        self.screen = screen
        
        #create a bullet at (0,0) and set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #store position of bullet in float
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        #bullet move upward
        #update position of bullet in float
        self.y -= self.speed_factor
        #update position of rect
        self.rect.y = self.y
        
    def draw_bullet(self):
        #draw bullet on screen
        pygame.draw.rect(self.screen, self.color, self.rect)