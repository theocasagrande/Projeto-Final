import pygame
import random
from os import path
from config import *
from assets import load_assets
from musica import tocar_musica_fundo


BLACK = (0, 0, 0)

def init_screen(window):
    assets = load_assets()

    base_font = assets['fontinit']
    texto = base_font.render("Pressione Enter para começar", True, (255, 0, 0))
    loading = base_font.render("Carregando...", True, (255, 0, 0))
    wizardimage = assets['wizard_idle'][0]
    knightimage = assets['knight_idle'][0]
    archerimage = assets['archer_idle'][0]
    tocar_musica_fundo()
    clock = pygame.time.Clock()
    running = True
    show_loading = False
    selectscreen = False
    player = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selectscreen = True
                elif event.key == pygame.K_ESCAPE:
                    return QUIT

        if selectscreen:
            window.fill(BLACK)

            # Posições dos personagens
            wizard_x = (WIDTH // 2 - wizardimage.get_width() // 2) - 100
            knight_x = (WIDTH // 2 - knightimage.get_width() // 2) + 100
            archer_x = (WIDTH // 2 - archerimage.get_width() // 2) + 0
            y_image = HEIGHT // 2 - wizardimage.get_height() // 2
            y_image_archer = (HEIGHT // 2 - archerimage.get_height() // 2) + 100

            window.blit(wizardimage, (wizard_x, y_image))
            window.blit(knightimage, (knight_x, y_image))
            window.blit(archerimage, (archer_x, y_image_archer))

            # Verifica se o mouse está sobre os textos
            font_size = 28
            hover_font_size = 34
            wizard_rect = pygame.Rect(wizard_x, y_image + wizardimage.get_height() + 10, 100, 40)
            knight_rect = pygame.Rect(knight_x, y_image + knightimage.get_height() + 10, 150, 40)
            archer_rect = pygame.Rect(archer_x, y_image_archer + archerimage.get_height() + 10, 150, 40)

            # Wizard select
            if wizard_rect.collidepoint(mouse_pos):
                font = pygame.font.Font(None, hover_font_size)
                if mouse_clicked[0]:  # Botão direito do mouse
                    player = "wizard"
                    selectscreen = False
                    show_loading = True
            else:
                font = pygame.font.Font(None, font_size)
            wizardselect = font.render("Mago", True, (255, 0, 0))
            window.blit(wizardselect, (wizard_x + wizardimage.get_width() // 2 - wizardselect.get_width() // 2, y_image + wizardimage.get_height() + 10))

            # Knight select
            if knight_rect.collidepoint(mouse_pos):
                font = pygame.font.Font(None, hover_font_size)
                if mouse_clicked[0]:
                    player = "knight"
                    selectscreen = False
                    show_loading = True
            else:
                font = pygame.font.Font(None, font_size)
            knightselect = font.render("Cavaleiro", True, (255, 0, 0))
            window.blit(knightselect, (knight_x + knightimage.get_width() // 2 - knightselect.get_width() // 2, y_image + knightimage.get_height() + 10))

            # Archer select
            if archer_rect.collidepoint(mouse_pos):
                font = pygame.font.Font(None, hover_font_size)
                if mouse_clicked[0]:  # Botão direito do mouse
                    player = "archer"
                    selectscreen = False
                    show_loading = True
            else:
                font = pygame.font.Font(None, font_size)
            archerselect = font.render("Arqueiro", True, (255, 0, 0))
            window.blit(archerselect, (archer_x + archerimage.get_width() // 2 - archerselect.get_width() // 2, y_image_archer + archerimage.get_height() + 10))

            pygame.display.flip()

        elif show_loading:
            window.fill(BLACK)
            window.blit(loading, (WIDTH // 2 - loading.get_width() // 2, HEIGHT // 2 - loading.get_height() // 2))
            pygame.display.flip()
            return GAME, player

        else:
            window.fill(BLACK)
            window.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - texto.get_height() // 2))
            pygame.display.flip()
            clock.tick(FPS)
