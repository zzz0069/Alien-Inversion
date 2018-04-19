class GameStats():
    #track game statistic information
    
    def __init__(self, ai_settings):
        #initial statistic information
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #active when game just start
        self.game_active = False
        self.high_score = 0
        
    def reset_stats(self):
        #initial those statistic information may change during running game
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
