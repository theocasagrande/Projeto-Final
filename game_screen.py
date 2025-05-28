import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from sprites import *
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
def game_screen(window, player):
    # ----- Inicia o jogo
    pygame.init()
    clock = pygame.time.Clock()

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
    bossteleport = pygame.sprite.Group()
    for tile_object in assets['map'].tmxdata.objects:
        if tile_object.name == 'wall':
            wall = Obstacle(tile_object.x * SCALE, tile_object.y * SCALE, tile_object.width * SCALE, tile_object.height * SCALE)
            all_sprites.add(wall)
            game_walls.add(wall)
    for tile_object in assets['map'].tmxdata.objects:
        if tile_object.name == 'player':
            if playerselected == 'knight':
                playerselected = Knight(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
            elif playerselected == 'wizard':
                playerselected = Wizard(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
            elif playerselected == 'archer':
                playerselected = Archer(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', all_sprites, game_walls, all_skeletons, all_projectiles)
        if tile_object.name == 'skeleton':
            skeleton1 = Skeleton(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', playerselected, game_walls, assets)
            all_skeletons.add(skeleton1)
            
        if tile_object.name == 'elite_orc':
            elite_orc1 = EliteOrc(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', playerselected, game_walls, assets)
            all_skeletons.add(elite_orc1)
        if tile_object.name == 'skeleton_archer':
            skeleton_archer1 = SkeletonArcher(tile_object.x * SCALE, tile_object.y * SCALE, 'idle', playerselected, game_walls, assets, enemy_projectiles)
            all_skeletons.add(skeleton_archer1)
        if tile_object.name == 'bossroom':
            bosstp = BossRoomTeleport(tile_object.x * SCALE, tile_object.y * SCALE, tile_object.width * SCALE, tile_object.height * SCALE)
            bossteleport.add(bosstp)
    

    camera = Camera(assets['map_width'], assets['map_height'])
    all_sprites.add(all_skeletons)
    all_sprites.add(all_projectiles)
    all_sprites.add(enemy_projectiles)
    all_sprites.add(bosstp)

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
                if event.key == pygame.K_l:
                    return BOSS, player, True

        for sprite in all_sprites:
            if isinstance(sprite, (Wizard, Knight, Archer, Skeleton, SkeletonArcher, SkeletonArcherArrow, EliteOrc, Arrow, ArrowSpecial)):
                sprite.update(dt)
            elif isinstance(sprite, (Obstacle, BossRoomTeleport)):
                continue  
            else:
                sprite.update()  

        camera.update(playerselected)
        now = pygame.time.get_ticks()
    

        selfhits = pygame.sprite.spritecollide(playerselected, all_skeletons, False, collide_hit_rect)
        if selfhits:
            for hit in selfhits:
                if not isinstance(hit, EliteOrc):
                    if now - playerselected.last_hit_time > 1000:  # 1000 ms = 1 segundo
                        hit.vel = vec(0, 0)
                        playerselected.state = 'hurt'
                        if hit.state != 'death':
                            playerselected.health -= MOB_DAMAGE
                        playerselected.last_hit_time = now  # Atualiza o tempo do último hit
            
        if playerselected.health <= 0:
            return RETRY, player, False
        window.blit(assets['map_surface'], camera.apply_rect(assets['map_rect']))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))
            # if not isinstance(sprite, Obstacle):
            #     if hasattr(sprite, 'hit_rect'):
            #         pygame.draw.rect(window, (255, 0, 0), camera.apply_rect(sprite.hit_rect), 1)
            #     else:
            #         pygame.draw.rect(window, (0, 255, 0), camera.apply_rect(sprite.rect), 1)


        teleport = pygame.sprite.spritecollide(playerselected, bossteleport, False, collide_hit_rect)
        if teleport:
            return BOSS, player, True
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