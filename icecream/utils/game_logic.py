from config import settings
import pygame
import random

# Globální proměnná pro assembled_items (circular imports)
_assembled_items = []

def get_assembled_items_global():
    """Vrací globální seznam assembled_items"""
    return _assembled_items

def set_assembled_items_global(items):
    """Nastaví globální seznam assembled_items"""
    global _assembled_items
    _assembled_items = items

def check_order_correctness(customer_queue):
    """Kontroluje správnost objednávky"""
    if not customer_queue or not _assembled_items:
        return False

    current_customer = customer_queue[0]
    recipe = {"cone": None, "scoops": []}
    
    for item in _assembled_items:
        if item.item_type == "cone" and item.item_key:
            recipe["cone"] = item.item_key
        elif item.item_type == "scoop" and item.item_key:
            recipe["scoops"].append(item.item_key)

    return (recipe['cone'] == current_customer.order.cone and 
            set(recipe['scoops']) == set(current_customer.order.scoops))

def reset_assembly(assembled_items):
    """Resetuje sestavování objednávky"""
    global _assembled_items
    for item in assembled_items:
        item.reset_position()
    assembled_items.clear()
    _assembled_items.clear()

def complete_order(customer_queue, assembled_items, all_sprites, game_state):
    """Dokončí objednávku"""
    global _assembled_items
    _assembled_items = assembled_items
    
    if not customer_queue:
        return

    if check_order_correctness(customer_queue):
        game_state.score += 1
        served_customer = customer_queue.pop(0)
        served_customer.serve()
        all_sprites.remove(served_customer)
        for i, customer in enumerate(customer_queue):
            customer.move_in_queue(i)
        reset_assembly(assembled_items)
        game_state.assembly_error = False
    else:
        game_state.assembly_error = True
        game_state.error_timer = pygame.time.get_ticks()

def add_new_customer(customer_queue, all_sprites, next_customer_id, window_width):
    """Přidá nového zákazníka do fronty"""
    from game_objects.customer import Customer  # Import zde kvůli circular imports
    
    if len(customer_queue) >= settings.MAX_CUSTOMERS_IN_QUEUE:
        return
    new_customer = Customer(len(customer_queue), window_width)
    customer_queue.append(new_customer)
    all_sprites.add(new_customer)
    next_customer_delay = random.randint(settings.NEW_CUSTOMER_DELAY_MIN, settings.NEW_CUSTOMER_DELAY_MAX)
    pygame.time.set_timer(pygame.USEREVENT + 2, next_customer_delay)

def return_to_menu(drag_items, assembled_items, customer_queue, all_sprites, game_state):
    """Návrat do menu s kompletním resetem"""
    # Kompletní reset všech herních prvků
    drag_items.clear()
    assembled_items.clear()
    customer_queue.clear()
    all_sprites.empty()
    
    # Reset všech herních proměnných
    game_state.reset()
    
    # Zrušení časovače pro nové zákazníky
    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
    
    return "menu"

def reset_game_completely(drag_items, assembled_items, customer_queue, all_sprites, game_state):
    """Kompletně resetuje hru pro nové kolo"""
    global _assembled_items
    
    # Reset všech seznamů a objektů
    for item in assembled_items:
        item.reset_position()
    assembled_items.clear()
    _assembled_items.clear()
    
    for item in drag_items:
        item.reset_position()
    
    customer_queue.clear()
    all_sprites.empty()
    
    # Reset všech proměnných KROMĚ final_score
    game_state.reset_for_new_game()
    
    # Zrušení všech časovačů
    pygame.time.set_timer(pygame.USEREVENT + 2, 0)

def initialize_game(width, height, scoop_images, cone_images, game_state):
    """Inicializuje hru s kompletním resetem"""
    from game_objects.draggable_item import DraggableItem  # Import zde kvůli circular imports
    
    global _assembled_items
    
    # Kompletní vyčištění před novým kolem
    _assembled_items.clear()
    
    game_state.game_start_time = pygame.time.get_ticks()  # Zaznamenání času začátku hry
    assembly_center = (width // 2 - 100, height // 2 + 50)
    
    drag_items = []
    
    # Kornouty ze spritesheet - VŠECHNY 4 TYPY
    cone_types = ['classic', 'waffle', 'short', 'sugar']
    for i, cone_type in enumerate(cone_types):
        if cone_type in cone_images:
            y_pos = 50 + (i * 60)
            cone_item = DraggableItem(
                cone_images[cone_type], 
                f"cone_{cone_type}", 
                (width - 290, y_pos),
                item_key=cone_type,
                item_type="cone",
                assembly_center=assembly_center
            )
            drag_items.append(cone_item)
    
    # Kopečky ze spritesheet - VŠECH 9 PŘÍCHUTÍ
    flavors_to_show = ['raspberry', 'pistachio', 'caramel', 'hazelnut', 'lemon', 'vanilla', 'peach', 'strawberry', 'chocolate']
    for i, flavor in enumerate(flavors_to_show):
        if flavor in scoop_images:
            y_pos = 50 + (i * 50)
            scoop_item = DraggableItem(
                scoop_images[flavor], 
                f"scoop_{flavor}", 
                (width - 150, y_pos),
                item_key=flavor,
                item_type="scoop",
                assembly_center=assembly_center
            )
            drag_items.append(scoop_item)
    
    return drag_items

def get_time_left(game_start_time):
    """Výpočet zbývajícího času"""
    if game_start_time == 0:
        return 60
    elapsed = (pygame.time.get_ticks() - game_start_time) // 1000
    return max(0, settings.GAME_DURATION_SECONDS - elapsed)