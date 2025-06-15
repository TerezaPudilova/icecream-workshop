import pygame


def load_icecream_decoration():
    """Načte obrázek zmrzlin a rozřeže ho na jednotlivé kornouty se zmrzlinou"""
    try:
        # OPRAVENO: Použití path_helper
        icecream_sheet = pygame.image.load("assets/Icecream/icecream_uvod_2.png").convert_alpha()
        
        sheet_width = icecream_sheet.get_width()
        sheet_height = icecream_sheet.get_height()
        
        # Lepší výpočet velikosti jedné zmrzliny s paddingem
        icecream_width = sheet_width // 5
        icecream_height = sheet_height
        
        icecreams = []
        
        # Rozřezání na 4 zmrzliny (vynecháváme první - nejvíc nalevo)
        for i in range(1, 5):  # Začínáme od indexu 1 místo 0
            # Individuální padding pro každou zmrzlinu
            if i == 1:  # První zmrzlina v našem seznamu (druhá v originále)
                # Více oříznutí zleva kvůli viditelné části předchozí zmrzliny
                padding_left = int(icecream_width * 0.15)  # Výrazně více zleva
                padding_right = int(icecream_width * 0.05)  # Standardně zprava
            else:
                # Ostatní zmrzliny - standardní padding
                padding_left = int(icecream_width * 0.05)   # Standardní zleva
                padding_right = int(icecream_width * 0.05)  # Standardní zprava
            
            padding_y = int(icecream_height * 0.02)  # 2% padding shora a zdola
            
            rect = pygame.Rect(
                i * icecream_width + padding_left, 
                padding_y, 
                icecream_width - padding_left - padding_right, 
                icecream_height - 2 * padding_y
            )
            icecream_surface = icecream_sheet.subsurface(rect)
            # Změna velikosti pro lepší použití v UI
            scaled_icecream = pygame.transform.scale(icecream_surface, (80, 120))
            icecreams.append(scaled_icecream)
                
        return icecreams
        
    except pygame.error:
        print("Nepodařilo se načíst obrázek zmrzlin pro dekoraci, používám placeholder...")
        # Vytvoření placeholder zmrzlin
        placeholders = []
        colors = [(255, 200, 150), (139, 69, 19), (144, 238, 144), (255, 182, 193), (255, 255, 224)]
        
        for color in colors:
            placeholder = pygame.Surface((80, 120), pygame.SRCALPHA)
            # Kornout
            pygame.draw.polygon(placeholder, (210, 180, 140), [(40, 30), (20, 115), (60, 115)])
            # Kopeček
            pygame.draw.circle(placeholder, color, (40, 35), 25)
            placeholders.append(placeholder)
        
        return placeholders

def load_scoop_spritesheet():
    """Načte spritesheet kopečků a extrahuje jednotlivé kopečky pomocí subsurface()"""
    try:
        # OPRAVENO: Použití path_helper
        spritesheet = pygame.image.load("assets/Icecream/download.png").convert_alpha()
        
        sheet_width = spritesheet.get_width()
        sheet_height = spritesheet.get_height()
        
        scoop_width = sheet_width // 3
        scoop_height = sheet_height // 3
        
        scoops = {}
        scoop_names = [
            ['raspberry', 'pistachio', 'caramel'],     # řádek 0: pozice 0, 1, 2
            ['hazelnut', 'lemon', 'vanilla'],          # řádek 1: pozice 3, 4, 5  
            ['peach', 'strawberry', 'chocolate']       # řádek 2: pozice 6, 7, 8
        ]
        
        for row in range(3):
            for col in range(3):
                # Výpočet pozice kopečku (0-8)
                position = row * 3 + col
                
                # Individuální oříznutí pro každý kopeček
                if position in [1, 4, 7]:  # pistachio (1), lemon (4), strawberry (7) - střední sloupec
                    # Střední kopečky - více oříznutí zprava kvůli přečuhování následujícího kopečku
                    padding_left = int(scoop_width * 0.06)
                    padding_right = int(scoop_width * 0.14)  # Výrazně více zprava
                    padding_y = int(scoop_height * 0.04)
                    
                    rect = pygame.Rect(
                        col * scoop_width + padding_left, 
                        row * scoop_height + padding_y, 
                        scoop_width - padding_left - padding_right, 
                        scoop_height - 2 * padding_y
                    )
                elif position in [2, 5, 8]:  # caramel (2), vanilla (5), chocolate (8) - pravý sloupec
                    # Pravé kopečky - méně oříznutí zleva, zachováme více z levé strany
                    padding_left = int(scoop_width * 0.02)   # Minimální zleva
                    padding_right = int(scoop_width * 0.08)  # Standardní zprava
                    padding_y = int(scoop_height * 0.04)
                    
                    rect = pygame.Rect(
                        col * scoop_width + padding_left, 
                        row * scoop_height + padding_y, 
                        scoop_width - padding_left - padding_right, 
                        scoop_height - 2 * padding_y
                    )
                else:  # position in [0, 3, 6] - raspberry, hazelnut, peach - levý sloupec
                    # Levé kopečky - standardní symetrické oříznutí
                    padding_x = int(scoop_width * 0.05)
                    padding_y = int(scoop_height * 0.02)
                    
                    rect = pygame.Rect(
                        col * scoop_width + padding_x, 
                        row * scoop_height + padding_y, 
                        scoop_width - 2 * padding_x, 
                        scoop_height - 2 * padding_y
                    )
                
                scoop_surface = spritesheet.subsurface(rect)
                scoop_name = scoop_names[row][col]
                scoops[scoop_name] = scoop_surface
                
        return scoops
        
    except pygame.error:
        print("Nepodařilo se načíst spritesheet kopečků, používám záložní obrázky...")
        try:
            return {
                'chocolate': pygame.image.load("assets/Icecream/cokoladova.png").convert_alpha(),
                'vanilla': pygame.image.load("assets/Icecream/smoulova.png").convert_alpha()
            }
        except pygame.error:
            print("Nepodařilo se načíst ani záložní obrázky, používám placeholdery...")
            # Vytvoříme placeholder kopečky
            placeholder_chocolate = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.circle(placeholder_chocolate, (139, 69, 19), (24, 24), 20)
            placeholder_vanilla = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.circle(placeholder_vanilla, (255, 255, 224), (24, 24), 20)
            return {
                'chocolate': placeholder_chocolate,
                'vanilla': placeholder_vanilla
            }

def load_cone_spritesheet():
    """Načte spritesheet kornoutů pomocí subsurface()"""
    try:
        # OPRAVENO: Použití path_helper
        spritesheet = pygame.image.load("assets/Icecream/cones.png").convert_alpha()
        
        sheet_width = spritesheet.get_width()
        sheet_height = spritesheet.get_height()
        
        # Předpokládám 4 kornouty v řadě (1x4)
        cone_width = sheet_width // 4
        cone_height = sheet_height
        
        cones = {}
        cone_names = ['classic', 'waffle', 'short', 'sugar']
        
        # Lepší oříznutí pro classic a waffle - odstranění černých artefaktů a lepší centrování
        for i in range(4):
            if i == 0:  # Classic kornout - více oříznutí zleva kvůli černým znakům
                padding_left = int(cone_width * 0.15)   # Více zleva - odstranění černých artefaktů
                padding_right = int(cone_width * 0.03)  # Minimální zprava pro zachování velikosti
                padding_y = int(cone_height * 0.04)     # Menší vertikální oříznutí
                
                rect = pygame.Rect(
                    i * cone_width + padding_left, 
                    padding_y, 
                    cone_width - padding_left - padding_right, 
                    cone_height - 2 * padding_y
                )
            elif i == 1:  # Waffle kornout - také více oříznutí zleva a méně zprava
                padding_left = int(cone_width * 0.12)   # Více zleva pro lepší centrování
                padding_right = int(cone_width * 0.02)  # Minimální zprava
                padding_y = int(cone_height * 0.04)     # Menší vertikální oříznutí
                
                rect = pygame.Rect(
                    i * cone_width + padding_left, 
                    padding_y, 
                    cone_width - padding_left - padding_right, 
                    cone_height - 2 * padding_y
                )
            else:  # Short a sugar kornouty - ponecháme původní nastavení (fungují dobře)
                padding_settings = {
                    2: {'x': int(cone_width * 0.12), 'y': int(cone_height * 0.06)},  # short  
                    3: {'x': int(cone_width * 0.08), 'y': int(cone_height * 0.05)}   # sugar
                }
                
                padding_x = padding_settings[i]['x']
                padding_y = padding_settings[i]['y']
                
                rect = pygame.Rect(
                    i * cone_width + padding_x, 
                    padding_y, 
                    cone_width - 2 * padding_x, 
                    cone_height - 2 * padding_y
                )
            
            cone_surface = spritesheet.subsurface(rect)
            cone_name = cone_names[i]
            cones[cone_name] = cone_surface
                
        return cones
        
    except pygame.error:
        print("Nepodařilo se načíst spritesheet kornoutů, používám záložní obrázek...")
        # Záložní načtení - vytvoříme více variant ze stejného obrázku
        # Záložní načtení - vytvoříme více variant ze stejného obrázku
        try:
            cone_img = pygame.image.load("assets/Icecream/kornout.png").convert_alpha()
            return {
                'classic': cone_img,
                'waffle': cone_img,  # V budoucnu můžete přidat různé kornouty
                'sugar': cone_img,
                'chocolate': cone_img
            }
        except pygame.error:
            print("Nepodařilo se načíst ani záložní kornout!")
            # Vytvoříme jednoduchý placeholder
            placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.polygon(placeholder, (210, 180, 140), [(32, 5), (10, 60), (54, 60)])
            return {'classic': placeholder}