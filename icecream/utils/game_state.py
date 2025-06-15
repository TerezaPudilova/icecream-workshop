class GameState:
    """Třída pro správu stavu hry"""
    
    def __init__(self):
        self.score = 0
        self.assembly_error = False
        self.error_timer = 0
        self.game_start_time = 0
        self.final_score = 0
        
    def reset(self):
        """Kompletní reset všech proměnných"""
        self.score = 0
        self.assembly_error = False
        self.error_timer = 0
        self.game_start_time = 0
        self.final_score = 0
        
    def reset_for_new_game(self):
        """Reset pro nové kolo (zachovává final_score)"""
        self.score = 0
        self.assembly_error = False
        self.error_timer = 0
        self.game_start_time = 0