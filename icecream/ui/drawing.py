import pygame
import math

def draw_gradient_background(surface, color1, color2, height):
    """Vykreslí vertikální gradient"""
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

def draw_fancy_button_no_shadow(surface, rect, text, font, hover=False):
    """Vykreslí vylepšené stylové tlačítko bez stínu"""
    # Animace tlačítka při hover
    if hover:
        # Zvětšení tlačítka při hover
        inflated_rect = rect.copy()
        inflated_rect.inflate_ip(8, 4)  # Mírné zvětšení
        working_rect = inflated_rect
    else:
        working_rect = rect
    
    # Složitější gradient pro tlačítko
    if hover:
        # Zlatavé barvy při hover
        color1 = (255, 215, 100)  # Zlatá světlá
        color2 = (255, 180, 50)   # Zlatá střední
        color3 = (220, 140, 30)   # Zlatá tmavá
        border_color = (180, 100, 20)
        text_color = (80, 40, 10)
    else:
        # Oranžové barvy normálně
        color1 = (255, 200, 120)  # Světle oranžová
        color2 = (255, 160, 80)   # Střední oranžová  
        color3 = (220, 120, 50)   # Tmavě oranžová
        border_color = (180, 80, 30)
        text_color = (100, 50, 20)
    
    # Složitější gradient se třemi barvami
    button_surface = pygame.Surface((working_rect.width, working_rect.height), pygame.SRCALPHA)
    for y in range(working_rect.height):
        if y < working_rect.height // 2:
            # Horní polovina: color1 -> color2
            ratio = y / (working_rect.height // 2)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        else:
            # Dolní polovina: color2 -> color3
            ratio = (y - working_rect.height // 2) / (working_rect.height // 2)
            r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
            g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
            b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
        pygame.draw.line(button_surface, (r, g, b), (0, y), (working_rect.width, y))
    
    # Vnější rámeček s gradientem
    pygame.draw.rect(surface, border_color, working_rect, border_radius=18, width=4)
    
    # Vnitřní světlý rámeček
    inner_border_rect = working_rect.copy()
    inner_border_rect.inflate_ip(-8, -8)
    pygame.draw.rect(surface, (255, 255, 255, 100), inner_border_rect, border_radius=15, width=2)
    
    # Aplikace gradientu
    inner_rect = working_rect.copy()
    inner_rect.inflate_ip(-4, -4)
    
    # Vytvoření masky pro zaoblené rohy
    mask_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, inner_rect.width, inner_rect.height), border_radius=15)
    
    # Aplikace masky na gradient
    button_surface = pygame.transform.scale(button_surface, (inner_rect.width, inner_rect.height))
    for y in range(inner_rect.height):
        for x in range(inner_rect.width):
            if mask_surface.get_at((x, y))[3] > 0:  # Pokud je pixel v masce viditelný
                surface.set_at((inner_rect.x + x, inner_rect.y + y), button_surface.get_at((x, y)))
    
    # Text s outline efektem
    # Outline (obrys textu)
    outline_positions = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]
    for dx, dy in outline_positions:
        outline_surface = font.render(text, True, (255, 255, 255, 150))
        outline_rect = outline_surface.get_rect(center=(working_rect.centerx + dx, working_rect.centery + dy))
        surface.blit(outline_surface, outline_rect)
    
    # Hlavní text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=working_rect.center)
    surface.blit(text_surface, text_rect)
    
    # Světelný efekt nahoře
    highlight_rect = pygame.Rect(working_rect.x + 10, working_rect.y + 8, working_rect.width - 20, 8)
    highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
    for x in range(highlight_rect.width):
        alpha = int(100 * (1 - abs(x - highlight_rect.width/2) / (highlight_rect.width/2)))
        highlight_surface.set_at((x, 0), (255, 255, 255, alpha))
        highlight_surface.set_at((x, 1), (255, 255, 255, alpha//2))
    surface.blit(highlight_surface, highlight_rect.topleft)
    
    return working_rect

def draw_fancy_title(surface, text, font, x, y, shadow_color=(100, 50, 50), main_color=(255, 220, 180)):
    """Vykreslí stylový titulek se stínem"""
    # Stín
    shadow_surface = font.render(text, True, shadow_color)
    surface.blit(shadow_surface, (x + 4, y + 4))
    
    # Hlavní text
    main_surface = font.render(text, True, main_color)
    surface.blit(main_surface, (x, y))

def draw_intro_screen(surface, floating_icecreams, decoration_icecreams, width, height):
    """Vykreslí tematickou úvodní obrazovku"""
    # Gradient pozadí (svetle modré k bílé)
    draw_gradient_background(surface, (200, 230, 255), (255, 255, 255), height)
    
    # Aktualizace a vykreslení plovoucích zmrzlin
    for icecream in floating_icecreams:
        icecream.update()
        icecream.draw(surface)
    
    # Hlavní titulek
    title_font = pygame.font.SysFont("arial", 60, bold=True)
    draw_fancy_title(surface, "Vítejte v Zmrzlinárně!", title_font, 
                    width // 2 - 300, height // 2 - 100)
    
    # Podtitulek
    subtitle_font = pygame.font.SysFont("arial", 24)
    subtitle_text = subtitle_font.render("Připravte se na sladké dobrodružství!", True, (150, 100, 50))
    surface.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, height // 2 - 20))
    
    # Dekorativní zmrzliny po stranách (jen 4 zmrzliny místo 5)
    if len(decoration_icecreams) >= 2:
        # Levá strana
        surface.blit(decoration_icecreams[0], (50, height // 2 - 60))
        surface.blit(decoration_icecreams[1], (100, height // 2 + 20))
        
        # Pravá strana - kontrola existence dalších zmrzlin
        if len(decoration_icecreams) >= 4:
            surface.blit(decoration_icecreams[2], (width - 130, height // 2 - 60))
            surface.blit(decoration_icecreams[3], (width - 180, height // 2 + 20))

def draw_menu_screen(surface, mouse_pos, decoration_icecreams, width, height):
    """Vykreslí tematické menu"""
    # Gradient pozadí (růžové k žluté)
    draw_gradient_background(surface, (255, 200, 220), (255, 240, 200), height)
    
    # Hlavní titulek menu
    title_font = pygame.font.SysFont("arial", 72, bold=True)
    draw_fancy_title(surface, "ZMRZLINÁRNA", title_font, 
                    width // 2 - 250, height // 2 - 150)
    
    # Stylové tlačítko HRÁT
    button_font = pygame.font.SysFont("arial", 36, bold=True)
    button_rect = pygame.Rect(width // 2 - 100, height // 2 - 20, 200, 60)  # Posunuto výš
    
    # Kontrola hover efektu
    hover = button_rect.collidepoint(mouse_pos)
    
    button_rect_result = draw_fancy_button_no_shadow(surface, button_rect, "HRÁT", button_font, hover)
    
    # Pouze 2 zmrzliny vedle tlačítka HRÁT
    if len(decoration_icecreams) >= 2:
        # Jen po stranách tlačítka
        surface.blit(decoration_icecreams[0], (button_rect.left - 120, button_rect.centery - 60))
        surface.blit(decoration_icecreams[1], (button_rect.right + 40, button_rect.centery - 60))
    
    return button_rect_result

def draw_assembly_zone(surface, assembly_zone, assembly_error, error_timer, panel_color, assembly_error_color, red, black, small_font):
    """Vykreslí oblast pro sestavování objednávky"""
    if assembly_error:
        if pygame.time.get_ticks() - error_timer < 3000:
            if (pygame.time.get_ticks() - error_timer) // 300 % 2 == 0:
                assembly_color = assembly_error_color
                border_color = red
            else:
                assembly_color = panel_color
                border_color = black
        else:
            assembly_color = panel_color
            border_color = black
    else:
        assembly_color = panel_color
        border_color = black
    
    pygame.draw.rect(surface, assembly_color, assembly_zone, border_radius=8)
    pygame.draw.rect(surface, border_color, assembly_zone, 2, border_radius=8)
    
    if assembly_error and pygame.time.get_ticks() - error_timer < 3000:
        assembly_title = small_font.render("CHYBNÁ OBJEDNÁVKA!", True, red)
    else:
        assembly_title = small_font.render("SESTAV OBJEDNÁVKU", True, black)
    surface.blit(assembly_title, (assembly_zone.centerx - assembly_title.get_width() // 2, assembly_zone.top - 25))

def draw_ingredient_panels(surface, drag_items, width, panel_color, section_font, small_font):
    """Vykresluje panely s ingrediencemi"""
    # Panel pro kornouty - VĚTŠÍ PRO 4 KORNOUTY
    cone_panel_rect = pygame.Rect(width - 300, 20, 135, 280)
    pygame.draw.rect(surface, panel_color, cone_panel_rect, border_radius=8)
    pygame.draw.rect(surface, (0, 0, 0), cone_panel_rect, 2, border_radius=8)
    
    cone_title = section_font.render("KORNOUTY", True, (100, 50, 150))
    surface.blit(cone_title, (cone_panel_rect.x + 10, cone_panel_rect.y + 10))
    
    # Panel pro kopečky - VĚTŠÍ PRO 9 KOPEČKŮ
    scoop_panel_rect = pygame.Rect(width - 160, 20, 135, 500)
    pygame.draw.rect(surface, panel_color, scoop_panel_rect, border_radius=8)
    pygame.draw.rect(surface, (0, 0, 0), scoop_panel_rect, 2, border_radius=8)
    
    scoop_title = section_font.render("KOPEČKY", True, (150, 100, 50))
    surface.blit(scoop_title, (scoop_panel_rect.x + 10, scoop_panel_rect.y + 10))
    
    # Mapování názvů
    flavor_names = {
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

    cone_names = {
        'classic': 'klasický',
        'waffle': 'vafle',
        'short': 'malý',
        'sugar': 'cukrový',
    }
    
    # Aktualizace a vykreslení ingrediencí s animacemi
    for item in drag_items:
        if not item.placed:
            item.update_animation()  # Aktualizace animací
            item.draw(surface)
    
    # Popisky se vykreslují POTÉ, co se vykreslí všechny ingredience
    for item in drag_items:
        if not item.placed and not item.dragging:  # Popisky jen pro ne-tažené ingredience
            # Popisky
            if item.item_type == "cone" and item.item_key:
                cone_text = small_font.render(cone_names[item.item_key], True, (0, 0, 0))
                surface.blit(cone_text, (item.rect.right + 5, item.rect.centery - 8))
            elif item.item_type == "scoop" and item.item_key:
                flavor_text = small_font.render(flavor_names[item.item_key], True, (0, 0, 0))
                surface.blit(flavor_text, (item.rect.right + 5, item.rect.centery - 8))

def draw_score(surface, score, assembly_center):
    """Vykreslí graficky zajímavé skóre"""
    # Pozadí pro skóre
    score_bg_rect = pygame.Rect(15, assembly_center[1] - 50, 200, 60)
    pygame.draw.rect(surface, (50, 50, 100), score_bg_rect, border_radius=10)
    pygame.draw.rect(surface, (100, 150, 255), score_bg_rect, 3, border_radius=10)
    
    # Gradient efekt (simulace pomocí více obdélníků)
    for i in range(5):
        alpha = 50 - i * 10
        gradient_rect = pygame.Rect(score_bg_rect.x + i, score_bg_rect.y + i, 
                                   score_bg_rect.width - 2*i, score_bg_rect.height - 2*i)
        gradient_surface = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient_surface.fill((100, 150, 255, alpha))
        surface.blit(gradient_surface, gradient_rect.topleft)
    
    # Titulek "SKÓRE"
    small_font = pygame.font.SysFont("arial", 16)
    score_title = small_font.render("SKÓRE", True, (200, 220, 255))
    title_x = score_bg_rect.x + (score_bg_rect.width - score_title.get_width()) // 2
    surface.blit(score_title, (title_x, score_bg_rect.y + 8))
    
    # Hlavní číslo skóre - větší font
    score_font = pygame.font.SysFont("arial", 28, bold=True)
    score_text = score_font.render(str(score), True, (255, 255, 100))
    score_x = score_bg_rect.x + (score_bg_rect.width - score_text.get_width()) // 2
    surface.blit(score_text, (score_x, score_bg_rect.y + 28))

def draw_timer(surface, time_left, assembly_center):
    """Vykreslí časomíru"""
    # Pozadí pro časomíru
    timer_bg_rect = pygame.Rect(15, assembly_center[1] - 130, 200, 60)
    
    # Barva pozadí se mění podle zbývajícího času
    if time_left > 30:
        bg_color = (50, 100, 50)  # Zelená
        border_color = (100, 255, 100)
    elif time_left > 15:
        bg_color = (100, 100, 50)  # Žlutá
        border_color = (255, 255, 100)
    else:
        bg_color = (100, 50, 50)  # Červená
        border_color = (255, 100, 100)
    
    pygame.draw.rect(surface, bg_color, timer_bg_rect, border_radius=10)
    pygame.draw.rect(surface, border_color, timer_bg_rect, 3, border_radius=10)
    
    # Gradient efekt
    for i in range(5):
        alpha = 50 - i * 10
        gradient_rect = pygame.Rect(timer_bg_rect.x + i, timer_bg_rect.y + i, 
                                   timer_bg_rect.width - 2*i, timer_bg_rect.height - 2*i)
        gradient_surface = pygame.Surface((gradient_rect.width, gradient_rect.height), pygame.SRCALPHA)
        gradient_surface.fill((*border_color, alpha))
        surface.blit(gradient_surface, gradient_rect.topleft)
    
    # Titulek "ČAS"
    small_font = pygame.font.SysFont("arial", 16)
    timer_title = small_font.render("ČAS", True, (200, 220, 255))
    title_x = timer_bg_rect.x + (timer_bg_rect.width - timer_title.get_width()) // 2
    surface.blit(timer_title, (title_x, timer_bg_rect.y + 8))
    
    # Zbývající čas - větší font
    timer_font = pygame.font.SysFont("arial", 28, bold=True)
    timer_text = timer_font.render(f"{time_left}s", True, (255, 255, 255))
    timer_x = timer_bg_rect.x + (timer_bg_rect.width - timer_text.get_width()) // 2
    surface.blit(timer_text, (timer_x, timer_bg_rect.y + 28))

def draw_final_score(surface, final_score, width, height):
    """Vykreslí stylové finální okno se skóre"""
    # Stejný gradient pozadí jako menu (růžové k žluté)
    draw_gradient_background(surface, (255, 200, 220), (255, 240, 200), height)
    
    # Hlavní titulek "ČAS VYPRŠEL!"
    title_font = pygame.font.SysFont("arial", 60, bold=True)
    draw_fancy_title(surface, "ČAS VYPRŠEL!", title_font, 
                    width // 2 - 220, height // 2 - 180, 
                    shadow_color=(80, 20, 20), main_color=(255, 150, 150))
    
    # Panel pro finální skóre ve stejném stylu jako tlačítka
    panel_width, panel_height = 500, 200
    panel_rect = pygame.Rect((width - panel_width) // 2, (height - panel_height) // 2, panel_width, panel_height)
    
    # Vykreslení fancy panelu
    draw_fancy_panel(surface, panel_rect)
    
    # "FINÁLNÍ SKÓRE" - menší titulek vycentrovaný
    subtitle_font = pygame.font.SysFont("arial", 28, bold=True)
    subtitle_text = "FINÁLNÍ SKÓRE"
    subtitle_surface = subtitle_font.render(subtitle_text, True, (255, 220, 180))
    subtitle_x = panel_rect.centerx - subtitle_surface.get_width() // 2
    draw_fancy_title(surface, subtitle_text, subtitle_font,
                    subtitle_x, panel_rect.y + 30,
                    shadow_color=(40, 40, 100), main_color=(255, 220, 180))
    
    # Samotné skóre - vycentrované v panelu
    score_font = pygame.font.SysFont("arial", 72, bold=True)
    score_text = str(final_score)
    score_surface = score_font.render(score_text, True, (255, 215, 100))
    score_x = panel_rect.centerx - score_surface.get_width() // 2
    draw_fancy_title(surface, score_text, score_font,
                    score_x, panel_rect.y + 80,
                    shadow_color=(100, 70, 20), main_color=(255, 215, 100))
    
    # Tlačítka zarovnaná s panelem
    button_font = pygame.font.SysFont("arial", 24, bold=True)
    
    button_width = 200
    button_spacing = 20
    
    total_buttons_width = button_width * 2 + button_spacing
    buttons_start_x = panel_rect.centerx - total_buttons_width // 2
    
    # Tlačítko "HRÁT"
    new_game_rect = pygame.Rect(buttons_start_x, height // 2 + 120, button_width, 50)
    mouse_pos = pygame.mouse.get_pos()
    hover_new = new_game_rect.collidepoint(mouse_pos)
    draw_fancy_button_no_shadow(surface, new_game_rect, "HRÁT", button_font, hover_new)
    
    # Tlačítko "ZPĚT DO MENU"
    menu_rect = pygame.Rect(buttons_start_x + button_width + button_spacing, height // 2 + 120, button_width, 50)
    hover_menu = menu_rect.collidepoint(mouse_pos)
    draw_fancy_button_no_shadow(surface, menu_rect, "ZPĚT DO MENU", button_font, hover_menu)
    
    # Stylové instrukce dole
    instruction_font = pygame.font.SysFont("arial", 18)
    instruction_text = "Použijte myš nebo klávesy Enter/Escape"
    instruction_surface = instruction_font.render(instruction_text, True, (150, 100, 50))
    instruction_x = width // 2 - instruction_surface.get_width() // 2
    surface.blit(instruction_surface, (instruction_x, height - 40))
    
    return new_game_rect, menu_rect

def draw_fancy_panel(surface, rect):
    """Vykreslí stylový panel ve stejném designu jako tlačítka"""
    # Gradient barvy pro panel (tmavě modré k světle modrým)
    color1 = (60, 80, 140)   # Tmavě modrá
    color2 = (100, 120, 180) # Střední modrá
    color3 = (140, 160, 220) # Světle modrá
    border_color = (40, 60, 120)
    
    # Složitější gradient se třemi barvami
    panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        if y < rect.height // 2:
            # Horní polovina: color1 -> color2
            ratio = y / (rect.height // 2)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        else:
            # Dolní polovina: color2 -> color3
            ratio = (y - rect.height // 2) / (rect.height // 2)
            r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
            g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
            b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
        pygame.draw.line(panel_surface, (r, g, b), (0, y), (rect.width, y))
    
    # Vnější rámeček
    pygame.draw.rect(surface, border_color, rect, border_radius=20, width=5)
    
    # Vnitřní světlý rámeček
    inner_border_rect = rect.copy()
    inner_border_rect.inflate_ip(-10, -10)
    pygame.draw.rect(surface, (200, 220, 255, 120), inner_border_rect, border_radius=15, width=3)
    
    # Aplikace gradientu s maskou pro zaoblené rohy
    inner_rect = rect.copy()
    inner_rect.inflate_ip(-5, -5)
    
    # Vytvoření masky pro zaoblené rohy
    mask_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, inner_rect.width, inner_rect.height), border_radius=15)
    
    # Aplikace masky na gradient
    panel_surface = pygame.transform.scale(panel_surface, (inner_rect.width, inner_rect.height))
    for y in range(inner_rect.height):
        for x in range(inner_rect.width):
            if mask_surface.get_at((x, y))[3] > 0:  # Pokud je pixel v masce viditelný
                surface.set_at((inner_rect.x + x, inner_rect.y + y), panel_surface.get_at((x, y)))
    
    # Světelný efekt nahoře
    highlight_rect = pygame.Rect(rect.x + 15, rect.y + 12, rect.width - 30, 12)
    highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
    for x in range(highlight_rect.width):
        alpha = int(80 * (1 - abs(x - highlight_rect.width/2) / (highlight_rect.width/2)))
        highlight_surface.set_at((x, 0), (255, 255, 255, alpha))
        highlight_surface.set_at((x, 1), (255, 255, 255, alpha//2))
    surface.blit(highlight_surface, highlight_rect.topleft)

def draw_controls_help(surface, state, height, section_font, small_font):
    """Zobrazí nápovědu ovládání"""
    help_texts = []
    
    if state == "menu":
        help_texts = [
            "OVLÁDÁNÍ:",
            "Enter - Spustit hru",
            "Escape - Ukončit hru"
        ]
    elif state == "playing":
        help_texts = [
            "OVLÁDÁNÍ:",
            "Enter - Dokončit objednávku",
            "Mezerník - Reset sestavování",
            "Escape - Návrat do menu"
        ]
    
    # Posun do levého spodního rohu
    y_start = height - (len(help_texts) * 20) - 10
    for i, text in enumerate(help_texts):
        if i == 0:  # Nadpis "OVLÁDÁNÍ" černě a tučně
            help_surface = section_font.render(text, True, (0, 0, 0))
        else:
            help_surface = small_font.render(text, True, (0, 0, 0))
        surface.blit(help_surface, (10, y_start + i * 20))