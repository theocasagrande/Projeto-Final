import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from spritestheo import Skeleton, Wizard, Wall
from spriteszaltron import *
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
    game_walls = pygame.sprite.Group()
    all_skeletons = pygame.sprite.Group()

    skeleton1 = Skeleton(500, 500, 'idle')
    for row, tiles in enumerate(assets['map']):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall = Wall(col, row)
                all_sprites.add(wall)
                game_walls.add(wall)
            if tile == 'P':
                wizard1 = Wizard(col, row, 'idle', all_sprites, game_walls)
                archer1 = Archer(col, row, 'idle', all_sprites, game_walls)
                all_sprites.add(wizard1)
                all_sprites.add(archer1)
    
    all_sprites.add(wizard1)
    all_sprites.add(archer1)
    all_skeletons.add(skeleton1)
    all_sprites.add(all_skeletons)
    # ----- Cria o relógio para controlar o FPS
    while state != DONE:
        clock.tick(FPS)

        dt = clock.tick(FPS) / 1000  # seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = DONE

        for sprite in all_sprites:
            if isinstance(sprite, Wizard):
                sprite.update(dt)
            elif isinstance(sprite, Archer):
                sprite.update(dt)
            else:
                sprite.update()

        window.fill((0, 0, 0))
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(window, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(window, LIGHTGRAY, (0, y), (WIDTH, y))
    

        all_sprites.draw(window)
        pygame.display.update()
    return state
# ----- Inicia estruturas de dados