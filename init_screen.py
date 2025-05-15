import pygame
import random
from os import path
from config import *
from assets import load_assets
BLACK = (0,0,0)
def init_screen(window):
    assets = load_assets()

    texto = assets['fontinit'].render("Pressione Enter para começar", True, (255, 0, 0))
    loading = assets['fontinit'].render("Carregando...", True, (255, 0, 0))

    clock = pygame.time.Clock()
    running = True
    show_loading = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_loading = True
                elif event.key == pygame.K_ESCAPE:
                    return QUIT

        if show_loading:
            window.fill(BLACK)
            window.blit(loading, (WIDTH // 2 - loading.get_width() // 2, HEIGHT // 2 - loading.get_height() // 2))
            pygame.display.flip()
            return GAME 
        else:
            window.fill(BLACK)
            window.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - texto.get_height() // 2))
            pygame.display.flip()
            clock.tick(FPS)


