import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from spritestheo import Skeleton, Wizard, Wall, Camera, Wizard_attack_ice
from spriteszaltron import *
# ----- Cores
vec = pygame.math.Vector2
def game_screen(window):
    # ----- Inicia o jogo
    pygame.init()
    clock = pygame.time.Clock()

    # ----- Carrega os assets
    assets = load_assets()

    FPS = 60
    DONE = 0
    PLAYING = 1
    state = PLAYING
    all_sprites = pygame.sprite.Group()
    game_walls = pygame.sprite.Group()
    all_skeletons = pygame.sprite.Group()
    all_projectiles = pygame.sprite.Group()
    for row, tiles in enumerate(assets['map'].data):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall = Wall(col, row)
                all_sprites.add(wall)
                game_walls.add(wall)
            if tile == 'P':
                wizard1 = Wizard(col, row, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
                archer1 = Archer(col, row, 'idle', all_sprites, game_walls)
                all_sprites.add(wizard1)
                all_sprites.add(archer1)
            if tile == 'S':
                skeleton1 = Skeleton(col, row, 'idle', wizard1)
                all_skeletons.add(skeleton1)
                all_sprites.add(skeleton1)
    camera = Camera(assets['map_width'], assets['map_height'])
    
    all_sprites.add(wizard1)
    all_sprites.add(archer1)
    all_sprites.add(all_skeletons)
    # ----- Cria o relógio para controlar o FPS
    while state != DONE:

        dt = clock.tick(FPS) / 1000  # seconds
        pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))
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
            elif isinstance(sprite, Skeleton):
                sprite.draw_health()
                sprite.update()
            else:
                sprite.update()
        camera.update(wizard1)
        for skeleton in all_skeletons:
            if skeleton.health <= 0:
                skeleton.kill()
            selfhits = pygame.sprite.spritecollide(wizard1, all_skeletons, False, pygame.sprite.collide_rect )
            for hit in selfhits:
                if wizard1.state != 'hurt':
                    wizard1.health -= MOB_DAMAGE
                    hit.vel = vec(0,0)
                    if wizard1.health <= 0:
                        return QUIT
        window.fill((169, 169, 169))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))
        pygame.display.update()
    return state

# ----- Inicia estruturas de dados