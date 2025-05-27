import pygame
import random
from os import path
from config import *
from assets import load_assets

BLACK = (0, 0, 0)

def winner_screen(window, player, enteredbossroom):
    assets = load_assets()

    base_font = assets['fontinit']
    derrotou = base_font.render("Você derrotou o BOSS", True, (255, 0, 0))
    parabens = base_font.render("Parabéns!", True, (255, 0, 0))

    clock = pygame.time.Clock()
    running = True
    

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return QUIT

        
        window.fill(BLACK)

        window.blit(derrotou, (WIDTH // 2 - derrotou.get_width() // 2, HEIGHT // 2 - derrotou.get_height() // 2))
        window.blit(parabens, (WIDTH // 2 - parabens.get_width() // 2, HEIGHT // 2 - parabens.get_height() // 2 + 100))
        pygame.display.flip()
        clock.tick(FPS)

