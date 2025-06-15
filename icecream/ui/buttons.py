from config import settings
from config.settings import *
import pygame

def create_buttons(assembly_center):
    """Vytvoří tlačítka pro hru"""
    button_width, button_height = settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT
    button_y = assembly_center[1] + 80
    
    done_button = pygame.Rect(assembly_center[0] - button_width - 10, button_y, button_width, button_height)
    reset_button = pygame.Rect(assembly_center[0] + 10, button_y, button_width, button_height)
    
    return done_button, reset_button

def draw_buttons(surface, done_button, reset_button, assembled_items, light_green, light_gray, light_red, black, button_font):
    """Vykreslí tlačítka HOTOVO a ZNOVU"""
    color = light_green if assembled_items else light_gray
    pygame.draw.rect(surface, color, done_button, border_radius=5)
    pygame.draw.rect(surface, black, done_button, 2, border_radius=5)
    
    done_text = button_font.render(settings.BUTTON_DONE, True, black)
    text_rect = done_text.get_rect(center=done_button.center)
    surface.blit(done_text, text_rect)
    
    pygame.draw.rect(surface, light_red, reset_button, border_radius=5)
    pygame.draw.rect(surface, black, reset_button, 2, border_radius=5)
    
    reset_text = button_font.render(settings.BUTTON_RESET, True, black)
    text_rect = reset_text.get_rect(center=reset_button.center)
    surface.blit(reset_text, text_rect)