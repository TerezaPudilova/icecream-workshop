#!/usr/bin/env python3
"""
Ukázka použití konstant z config/settings.py
"""

from config import settings
from config.settings import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT

# Příklady použití:

# 1. Rozměry okna
print(f"Rozměry okna: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# 2. Barvy  
background_color = WHITE
text_color = BLACK

# 3. Pozice
assembly_center = settings.ASSEMBLY_CENTER
customer_pos = settings.get_customer_position(0)

# 4. Herní konstanty
max_customers = settings.MAX_CUSTOMERS_IN_QUEUE
game_duration = settings.GAME_DURATION_SECONDS

# 5. Fonty (po pygame.init())
import pygame
pygame.init()
fonts = settings.init_fonts()
title_font = fonts['main_title']

print("✅ Všechny konstanty načteny správně!")
