import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from spritestheo import *
# ----- Cores

def game_screen(window):
    # ----- Inicia o jogo
    pygame.init()
    clock = pygame.time.Clock()

    # ----- Carrega os assets
    assets = load_assets()

    FPS = 45
    DONE = 0
    PLAYING = 1
    state = PLAYING
    all_sprites = pygame.sprite.Group()
    all_skeletons = pygame.sprite.Group()
    skeleton1 = Skeleton(random.randint(100,500), random.randint(100,500), 'idle')
    all_skeletons.add(skeleton1)
    all_sprites.add(all_skeletons)
    # ----- Cria o relógio para controlar o FPS
    while state != DONE:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = DONE
        all_sprites.update()
        window.fill((255,255, 255))
        all_sprites.draw(window)
        pygame.display.update()
    return state
# ----- Inicia estruturas de dados