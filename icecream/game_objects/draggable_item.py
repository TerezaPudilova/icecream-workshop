import pygame
import math

class DraggableItem:
    def __init__(self, image, label, start_pos, item_key=None, item_type="scoop", assembly_center=(600, 400)):
        self.original_image = image
        self.image = pygame.transform.scale(image, (48, 48))
        self.label = label
        self.item_key = item_key  # klíč pro identifikaci (flavor pro scoop, cone_type pro cone)
        self.item_type = item_type  # "scoop" nebo "cone"
        self.start_pos = start_pos
        self.rect = self.image.get_rect(topleft=start_pos)
        self.dragging = False
        self.offset = (0, 0)
        self.placed = False
        self.assembly_center = assembly_center
        
        # Animace
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.bounce_offset = 0
        self.bounce_speed = 0.1

    def update_animation(self):
        """Aktualizuje animace pro předmět"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover efekt - zvětšení při najetí myší
        if self.rect.collidepoint(mouse_pos) and not self.placed:
            self.target_scale = 1.2
        else:
            self.target_scale = 1.0
        
        # Plynulé přechody měřítka
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * 0.15
        
        # Bounce animace pro umístěné předměty
        if self.placed:
            self.bounce_offset += self.bounce_speed
            if self.bounce_offset > 6.28:  # 2*π
                self.bounce_offset = 0

    def draw(self, surface):
        # Aplikace animací při vykreslování
        if self.placed:
            # Žádné animace pro umístěné předměty - jen standardní vykreslení
            draw_pos = self.rect.topleft
        else:
            # Hover efekt pro neumístěné předměty
            if abs(self.hover_scale - 1.0) > 0.01:
                scaled_size = int(48 * self.hover_scale)
                scaled_image = pygame.transform.scale(self.original_image, (scaled_size, scaled_size))
                # Vycentrování zvětšeného obrázku
                center_offset = (48 - scaled_size) // 2
                draw_pos = (self.rect.x + center_offset, self.rect.y + center_offset)
                surface.blit(scaled_image, draw_pos)
                return
            else:
                draw_pos = self.rect.topleft
        
        surface.blit(self.image, draw_pos)

    def reset_position(self):
        self.rect.topleft = self.start_pos
        self.placed = False
        self.dragging = False
        self.bounce_offset = 0

    def handle_event(self, event, assembled_items):
        """Upravená verze - assembled_items se předává jako parametr"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.placed:
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                assembly_zone = pygame.Rect(self.assembly_center[0] - 50, self.assembly_center[1] - 150, 100, 200)
                if assembly_zone.colliderect(self.rect):
                    # Kornouty jdou dolů, kopečky nahoru
                    if self.item_type == "cone":
                        self.rect.center = (self.assembly_center[0], self.assembly_center[1] + 20)
                    else:
                        self.rect.center = (self.assembly_center[0], self.assembly_center[1] - len([item for item in assembled_items if item.item_type == "scoop"]) * 25)
                    assembled_items.append(self)
                    self.placed = True
                else:
                    self.reset_position()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset[0]
                self.rect.y = mouse_y + self.offset[1]