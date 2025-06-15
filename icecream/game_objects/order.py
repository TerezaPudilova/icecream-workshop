import random

class Order:
    def __init__(self):
        # Mapování názvů
        self.flavor_names = {
            'raspberry': 'malina',
            'pistachio': 'pistácie', 
            'caramel': 'karamel',
            'hazelnut': 'oříšek',
            'lemon': 'citrón',
            'vanilla': 'vanilka',
            'peach': 'meruňka',
            'strawberry': 'jahoda',
            'chocolate': 'čokoláda'
        }

        self.cone_names = {
            'classic': 'klasický',
            'waffle': 'vafle',
            'short': 'malý',
            'sugar': 'cukrový',
        }
        
        # Výběr kornoutu ze spritesheet
        available_cones = list(self.cone_names.keys())
        self.cone = random.choice(available_cones)
        
        # Výběr kopečků
        available_flavors = list(self.flavor_names.keys())
        num_scoops = random.randint(1, 3)
        self.scoops = random.sample(available_flavors, num_scoops)

    def get_text(self):
        czech_cone = self.cone_names[self.cone]
        czech_flavors = [self.flavor_names[flavor] for flavor in self.scoops]
        return f"{czech_cone} kornout, {', '.join(czech_flavors)}"