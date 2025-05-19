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

def draw_player_health(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = (0, 255, 0)
    elif pct > 0.3:
        col = (255, 255, 0)
    else:
        col = (255, 0, 0)
    pygame.draw.rect(surface, col, fill_rect)
    pygame.draw.rect(surface, (255,255,255), outline_rect, 2)
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
    # for row, tiles in enumerate(assets['map'].data):
    #     for col, tile in enumerate(tiles):
    #         if tile == '1':
    #             wall = Wall(col, row)
    #             all_sprites.add(wall)
    #             game_walls.add(wall)
    #         if tile == 'P':
    #             wizard1 = Wizard(col, row, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
    #             archer1 = Archer(col, row, 'idle', all_sprites, game_walls)
    #             all_sprites.add(wizard1)
    #             all_sprites.add(archer1)
    #         if tile == 'S':
    #             skeleton1 = Skeleton(col, row, 'idle', wizard1, game_walls)
    #             all_skeletons.add(skeleton1)
    #             all_sprites.add(skeleton1)
    wizard1 = Wizard(10, 5, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
    camera = Camera(assets['map_width'], assets['map_height'])
    skeleton1 = Skeleton(15, 15, 'idle', wizard1, game_walls)
    skeleton2 = Skeleton(20, 15, 'idle', wizard1, game_walls)
    skeleton3 = Skeleton(15, 20, 'idle', wizard1, game_walls)
    all_skeletons.add(skeleton1)
    all_skeletons.add(skeleton2)
    all_skeletons.add(skeleton3)
    all_sprites.add(wizard1)
    # all_sprites.add(archer1)
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
                sprite.update(dt)
            else:
                sprite.update()
        camera.update(wizard1)
        for skeleton in all_skeletons:
            if skeleton.health <= 0:
                skeleton.kill()
            selfhits = pygame.sprite.spritecollide(wizard1, all_skeletons, False, pygame.sprite.collide_rect )
            for hit in selfhits:
                    wizard1.health -= MOB_DAMAGE
                    hit.vel = vec(0,0)
                    wizard1.state = 'hurt'
                    if wizard1.health <= 0:
                        return QUIT
            if selfhits:
                wizard1.pos += vec(MOB_KNOCKBACK).rotate(-selfhits[0].rot)
        
        window.blit(assets['map_surface'], camera.apply_rect(assets['map_rect']))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))

        for skeleton in all_skeletons:
            # Calculate health bar position relative to camera
            pos = camera.apply(skeleton)
            health_pos = pygame.Rect(pos.x, pos.y - 10, skeleton.rect.width, 5)
            
            # Draw background (empty) health bar
            pygame.draw.rect(window, (255, 0, 0), health_pos)
            
            health_width = (skeleton.health / SKELETON_HEALTH) * skeleton.rect.width
            current_health_pos = pygame.Rect(pos.x, pos.y - 10, health_width, 5)
            pygame.draw.rect(window, (0, 255, 0), current_health_pos)


        draw_player_health(window, 10, 10, wizard1.health / PLAYER_HEALTH)
        pygame.display.update()
    return state

# ----- Inicia estruturas de dados