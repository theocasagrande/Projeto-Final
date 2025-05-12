import pygame
import random
from os import path
from config import *
from assets import load_assets
# ----- Cores

def game_screen(window):
    # ----- Inicia o jogo
    pygame.init()
    clock = pygame.time.Clock()
    game = True

    # ----- Carrega os assets
    assets = load_assets()

    FPS = 60
    DONE = 0
    PLAYING = 1
    state = PLAYING
    # ----- Cria o relógio para controlar o FPS
    while state != DONE:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = DONE
        window.fill((255,255, 255))
        pygame.display.update()
    return state
# ----- Inicia estruturas de dados