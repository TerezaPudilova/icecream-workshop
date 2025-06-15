import random
from config import settings

class Order:
    def __init__(self):
        # Mapování názvů
        self.flavor_names = settings.FLAVOR_NAMES 

        self.cone_names = settings.CONE_NAMES 
        
        # Výběr kornoutu ze spritesheet
        available_cones = list(self.cone_names.keys())
        self.cone = random.choice(available_cones)
        
        # Výběr kopečků
        available_flavors = list(self.flavor_names.keys())
        num_scoops = random.randint(settings.MIN_SCOOPS_PER_ORDER, settings.MAX_SCOOPS_PER_ORDER)
        self.scoops = random.sample(available_flavors, num_scoops)

    def get_text(self):
        czech_cone = self.cone_names[self.cone]
        czech_flavors = [self.flavor_names[flavor] for flavor in self.scoops]
        return f"{czech_cone} kornout, {', '.join(czech_flavors)}"