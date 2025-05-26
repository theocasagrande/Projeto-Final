import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from spritestheo import *
from spriteszaltron import *
from spritesbruno import *
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
def boss_room(window, player):
    # ----- Inicia o jogo
    pygame.init()
    clock = pygame.time.Clock()

    print(player)
    # ----- Carrega os assets
    assets = load_assets()
    playerselected = player

    FPS = 60
    DONE = 0
    PLAYING = 1
    state = PLAYING
    all_sprites = pygame.sprite.LayeredUpdates()
    game_walls = pygame.sprite.Group()
    all_skeletons = pygame.sprite.Group()
    all_projectiles = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()

    
      # instância real do jogador

    playerselected = None  # será instanciado em seguida

# Primeiro passo: cria jogador e paredes
    for tile_object in assets['bossroom'].tmxdata.objects:
        if tile_object.name == 'player':
            if player == 'knight':
                playerselected = Knight(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
            elif player == 'wizard':
                playerselected = Wizard(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
            elif player == 'archer':
                playerselected = Archer(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
        elif tile_object.name == 'wall':
            wall = Obstacle(tile_object.x * SCALE, tile_object.y * SCALE,
                            tile_object.width * SCALE, tile_object.height * SCALE)
            all_sprites.add(wall)
            game_walls.add(wall)

    # Segundo passo: cria o boss, agora com playerselected já instanciado
    for tile_object in assets['bossroom'].tmxdata.objects:
        if tile_object.name == 'boss_spawn' and playerselected is not None:
            boss = Necromancer(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                            playerselected, game_walls, all_skeletons, assets, enemy_projectiles)
            all_sprites.add(boss)
            all_skeletons.add(boss)


            
    

    camera = Camera(assets['bossroom_width'], assets['bossroom_height'])
    all_sprites.add(all_skeletons)
    all_sprites.add(all_projectiles)
    all_sprites.add(enemy_projectiles)
    

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
            elif isinstance(sprite, Knight):
                sprite.update(dt)
            elif isinstance(sprite, Archer):
                sprite.update(dt)
            elif isinstance(sprite, Skeleton):
                sprite.update(dt)
            elif isinstance(sprite, SkeletonArcher):
                sprite.update(dt)
            elif isinstance(sprite, SkeletonArcherArrow):
                sprite.update(dt)
            elif isinstance(sprite, NecromancerAttack3):
                sprite.update(dt)
            elif isinstance(sprite, Archer):
                sprite.update(dt)
            elif isinstance(sprite, Arrow):
                sprite.update(dt)
            elif isinstance(sprite, ArrowSpecial):
                sprite.update(dt)
            elif isinstance(sprite, Obstacle):
                continue
            elif isinstance(sprite, BossRoomTeleport):
                continue
            elif isinstance(sprite, Necromancer):
                sprite.update(dt)
            else:
                sprite.update()
        camera.update(playerselected)
        now = pygame.time.get_ticks()
    

        selfhits = pygame.sprite.spritecollide(playerselected, all_skeletons, False, collide_hit_rect)
        if selfhits:
            for hit in selfhits:
                if now - playerselected.last_hit_time > 1000:  # 1000 ms = 1 segundo
                    playerselected.health -= MOB_DAMAGE
                    hit.vel = vec(0, 0)
                    playerselected.state = 'hurt'
                    playerselected.last_hit_time = now  # Atualiza o tempo do último hit
        
        if playerselected.health <= 0:
            return QUIT
        window.blit(assets['bossroom_surface'], camera.apply_rect(assets['bossroom_rect']))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))
            if not isinstance(sprite, Obstacle):
                if hasattr(sprite, 'hit_rect'):
                    pygame.draw.rect(window, (255, 0, 0), camera.apply_rect(sprite.hit_rect), 1)
                else:
                    pygame.draw.rect(window, (0, 255, 0), camera.apply_rect(sprite.rect), 1)

        for skeleton in all_skeletons:
            # Calculate health bar position relative to camera
            pos = camera.apply(skeleton)
            health_pos = pygame.Rect(pos.x, pos.y - 10, skeleton.rect.width, 5)
            
            # Draw background (empty) health bar
            pygame.draw.rect(window, (255, 0, 0), health_pos)
            
            health_width = (skeleton.health / skeleton.total_health) * skeleton.rect.width
            current_health_pos = pygame.Rect(pos.x, pos.y - 10, health_width, 5)
            pygame.draw.rect(window, (0, 255, 0), current_health_pos)

        draw_player_health(window, 10, 10, playerselected.health / playerselected.total_health)
        pygame.display.update()
    return state


# ----- Inicia estruturas de dados