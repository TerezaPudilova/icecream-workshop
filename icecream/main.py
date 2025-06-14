import pygame
import sys

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Testovací hra")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 200, 200))  # zatím nic :D jen světle růžový pozadí
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
