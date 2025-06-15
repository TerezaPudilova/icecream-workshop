#!/usr/bin/env python3
"""
Pracovní verze main.py s opraveným importem
Všechny importy by měly fungovat podle diagnostiky
"""

import pygame
import sys
import random
import os

# Import konfigurace
from config import settings
from config.settings import *


print("🚀 Spouštím hlavní hru...")
print(f"📁 Pracovní adresář: {os.getcwd()}")

# Test importu před spuštěním
try:
    print("📦 Testování importů...")
    
    from game_objects.draggable_item import DraggableItem
    from game_objects.customer import Customer
    from game_objects.order import Order
    from game_objects.floating_icecream import FloatingIcecream
    print("✅ game_objects - úspěšně naimportováno")
    
    from ui.drawing import *
    from ui.buttons import create_buttons, draw_buttons
    print("✅ ui - úspěšně naimportováno")
    
    from utils.asset_loader import load_scoop_spritesheet, load_cone_spritesheet, load_icecream_decoration
    from utils.game_logic import *
    from utils.game_state import GameState
    print("✅ utils - úspěšně naimportováno")
    
    print("🎉 Všechny moduly úspěšně načteny!")
    
except ImportError as e:
    print(f"❌ Import selhal: {e}")
    print("🛑 Ukončuji program")
    sys.exit(1)

# Inicializace Pygame
pygame.init()

# Globální proměnná
global final_score

# Nastavení velikosti okna
WIDTH, HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

ASSEMBLY_CENTER = settings.ASSEMBLY_CENTER

# FPS a časovač
clock = pygame.time.Clock()
FPS = settings.FPS

print("🎨 Načítám grafické assety...")

# Inicializace fontů
fonts = init_fonts()
font = fonts['main_title']
small_font = fonts['small']
button_font = fonts['button']
order_font = fonts['order']
section_font = fonts['section']


# Načtení obrázků
scoop_images = load_scoop_spritesheet()
cone_images = load_cone_spritesheet()

# Načtení dekoračních zmrzlin a vytvoření plovoucích animací
decoration_icecreams = load_icecream_decoration()
floating_icecreams = []

# Vytvoření plovoucích zmrzlin pro pozadí
for _ in range(8):
    if decoration_icecreams:
        img = random.choice(decoration_icecreams)
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        floating_icecreams.append(FloatingIcecream(img, x, y))

print("🎮 Inicializuji herní stav...")

# Inicializace herního stavu
game_state = GameState()

def main():
    global final_score
    
    print("🎯 Vstupuji do hlavní herní smyčky...")
    
    STATE = "intro"
    drag_items = []
    assembled_items = []
    customer_queue = []
    next_customer_id = 0
    all_sprites = pygame.sprite.Group()
    intro_start_time = pygame.time.get_ticks()
    button_rect_global = pygame.Rect(0, 0, 0, 0)
    final_score = 0

    done_button, reset_button = create_buttons(ASSEMBLY_CENTER)

    print("🔄 Spouštím hlavní smyčku...")

    # --- Hlavní smyčka ---
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.USEREVENT + 2:
                add_new_customer(customer_queue, all_sprites, next_customer_id, WIDTH)

            # Ovládání klávesnicí
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if STATE == "playing":
                        STATE = return_to_menu(drag_items, assembled_items, customer_queue, all_sprites, game_state)
                    elif STATE == "menu":
                        running = False
                    elif STATE == "game_over":
                        STATE = return_to_menu(drag_items, assembled_items, customer_queue, all_sprites, game_state)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if STATE == "menu":
                        drag_items = initialize_game(WIDTH, HEIGHT, scoop_images, cone_images, game_state)
                        STATE = "playing"
                        add_new_customer(customer_queue, all_sprites, next_customer_id, WIDTH)
                    elif STATE == "game_over":
                        drag_items = initialize_game(WIDTH, HEIGHT, scoop_images, cone_images, game_state)
                        STATE = "playing"
                        add_new_customer(customer_queue, all_sprites, next_customer_id, WIDTH)
                    elif STATE == "playing" and assembled_items:
                        complete_order(customer_queue, assembled_items, all_sprites, game_state)
                elif event.key == pygame.K_SPACE:
                    if STATE == "playing":
                        reset_assembly(assembled_items)
                        
            elif STATE == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect_global.collidepoint(event.pos):
                        drag_items = initialize_game(WIDTH, HEIGHT, scoop_images, cone_images, game_state)
                        STATE = "playing"
                        add_new_customer(customer_queue, all_sprites, next_customer_id, WIDTH)
                        
            elif STATE == "game_over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    panel_width = 500
                    button_width = 200
                    button_spacing = 20
                    total_buttons_width = button_width * 2 + button_spacing
                    buttons_start_x = (WIDTH // 2) - total_buttons_width // 2
                    
                    new_game_rect = pygame.Rect(buttons_start_x, HEIGHT // 2 + 120, button_width, 50)
                    menu_rect = pygame.Rect(buttons_start_x + button_width + button_spacing, HEIGHT // 2 + 120, button_width, 50)
                    
                    if new_game_rect.collidepoint(mouse_pos):
                        drag_items = initialize_game(WIDTH, HEIGHT, scoop_images, cone_images, game_state)
                        STATE = "playing"
                        add_new_customer(customer_queue, all_sprites, next_customer_id, WIDTH)
                    elif menu_rect.collidepoint(mouse_pos):
                        STATE = return_to_menu(drag_items, assembled_items, customer_queue, all_sprites, game_state)
                        
            elif STATE == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if done_button.collidepoint(event.pos) and assembled_items:
                        complete_order(customer_queue, assembled_items, all_sprites, game_state)
                    elif reset_button.collidepoint(event.pos):
                        reset_assembly(assembled_items)
                
                for item in drag_items:
                    item.handle_event(event, assembled_items)

        # Vykreslování
        screen.fill(settings.WHITE)
        
        if STATE == "intro":
            draw_intro_screen(screen, floating_icecreams, decoration_icecreams, WIDTH, HEIGHT)
            if pygame.time.get_ticks() - intro_start_time > 4000:
                STATE = "menu"

        elif STATE == "menu":
            mouse_pos = pygame.mouse.get_pos()
            button_rect_global = draw_menu_screen(screen, mouse_pos, decoration_icecreams, WIDTH, HEIGHT)
            draw_controls_help(screen, "menu", HEIGHT, section_font, small_font)

        elif STATE == "playing":
            time_left = get_time_left(game_state.game_start_time)
            if time_left <= 0:
                final_score = game_state.score
                reset_game_completely(drag_items, assembled_items, customer_queue, all_sprites, game_state)
                STATE = "game_over"
            
            all_sprites.update()
            all_sprites.draw(screen)

            # Vykreslení oblasti pro sestavování
            assembly_zone = pygame.Rect(ASSEMBLY_CENTER[0] - 50, ASSEMBLY_CENTER[1] - 150, 100, 200)
            
            draw_assembly_zone(screen, assembly_zone, game_state.assembly_error, game_state.error_timer, 
                             PANEL_COLOR, ASSEMBLY_ERROR, RED, BLACK, small_font)

            for item in assembled_items:
                item.draw(screen)

            draw_ingredient_panels(screen, drag_items, WIDTH, PANEL_COLOR, section_font, small_font)
            draw_buttons(screen, done_button, reset_button, assembled_items, LIGHT_GREEN, LIGHT_GRAY, 
                        LIGHT_RED, BLACK, button_font)

            draw_score(screen, game_state.score, ASSEMBLY_CENTER)
            draw_timer(screen, time_left, ASSEMBLY_CENTER)

            for customer in customer_queue:
                customer.draw_order(screen)

            if customer_queue:
                queue_text = small_font.render(f"Zákazníků ve frontě: {len(customer_queue)}", True, BLACK)
                screen.blit(queue_text, (20, 70))
            
            draw_controls_help(screen, "playing", HEIGHT, section_font, small_font)
        
        elif STATE == "game_over":
            new_game_rect, menu_rect = draw_final_score(screen, final_score, WIDTH, HEIGHT)

        pygame.display.flip()

    print("👋 Hra končí...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Chyba během hry: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()