class Settings():
    #store all settings
    
    
    def __init__(self):
        #initial settings
        
        #screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230,230,230)
        self.ship_speed_factor = 1.5
        
        #bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 8
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3
        
        #alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        
        #speed up in a scale
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
        #fleet_direction:move right while =1, =-1 while move left
        self.fleet_direction = 1
        
        #ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
    def initialize_dynamic_settings(self):
        #initial dynamic change of the game
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 50
        
        
    def increase_speed(self):
        #speed up setting
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
