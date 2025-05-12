import pygame
import random
from os import path
from config import IMG_DIR, FPS, GAME, QUIT, WIDTH
from assets import load_assets
BLACK = (0,0,0)
def init_screen(window):
    
    assets = load_assets()

    texto = assets['fontinit'].render("Pressione Enter para começar", True, (255, 0, 0))
    # Cria um relógio para controlar o FPS
    clock = pygame.time.Clock()
    running = True
    # Loop principal da tela inicial
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = GAME
                    running = False

        # Desenha o fundo
        window.fill(BLACK)

        # Renderiza o texto "Press Enter to Start"
        window.blit(texto, (WIDTH // 2 - texto.get_width() // 2, 500))

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(FPS)
    return state
