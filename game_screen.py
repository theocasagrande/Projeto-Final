import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from sprites import *
from musica import parar_musica
vec = pygame.math.Vector2

# Desenha a barra de vida do personagem
def draw_player_health(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    # Desenha os rects do outline e da barra de vida
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    if pct > 0.6:
        # Se o jogador tiver com mais de 60% de sua vida total, a barra fica verde
        col = (0, 255, 0)
    elif pct > 0.3:
        # Se a vida do jogador estiver entre 30% e 60% de sua vida total, a barra fica amarela
        col = (255, 255, 0)
    else:
        # Se a vida do jogador for menor que 30% de sua vida total, a barra fica vermelha
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

    #Leitura do arquivo do mapa e criação das paredes, o personagem e inimigos
    # Posiciona cada sprite de acordo com a posição do objeto no arquivo do mapa
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
    
    # Cria a camera
    camera = Camera(assets['map_width'], assets['map_height'])
    all_sprites.add(all_skeletons)
    all_sprites.add(all_projectiles)
    all_sprites.add(enemy_projectiles)
    all_sprites.add(bosstp)

    while state != DONE:

        dt = clock.tick(FPS) / 1000  # seconds
        pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))
        # Fecha o jogo se o jogador apertar ESC ou o X na aba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = DONE
        # Atualiza o estado de cada sprite
        for sprite in all_sprites:
            if isinstance(sprite, (Wizard, Knight, Archer, Skeleton, SkeletonArcher, SkeletonArcherArrow, EliteOrc, Arrow, ArrowSpecial)):
                sprite.update(dt)
            elif isinstance(sprite, (Obstacle, BossRoomTeleport)):
                continue  
            else:
                sprite.update()  
        # Atualiza a posição da camera
        camera.update(playerselected)
        now = pygame.time.get_ticks()
    
        # Verifica colisão entre personagem e inimigo e aplica dano no personagem
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
        # Se vida do jogador acabar, muda a cena para a tela de tentar de novo
        if playerselected.health <= 0:
            return RETRY, player, False
        # Desenha os sprites na tela de acordo com a posição da camera
        window.blit(assets['map_surface'], camera.apply_rect(assets['map_rect']))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))

        #Teletransporta o personagem para a sala do boss quando ele tocar no rect do sprite de teleport
        teleport = pygame.sprite.spritecollide(playerselected, bossteleport, False, collide_hit_rect)
        if teleport:
            parar_musica()
            return BOSS, player, True
        # Desenha a barra de vida dos inimigos
        for skeleton in all_skeletons:
            # Calcula a posição da barra de vida de acordo com a posição da camera
            pos = camera.apply(skeleton)
            health_pos = pygame.Rect(pos.x, pos.y - 10, skeleton.rect.width, 5)
            
            # Desenha o background da barra de vida (vermelha)
            pygame.draw.rect(window, (255, 0, 0), health_pos)
            
            # Desenha a barra de vida variando seu tamanho de acordo com a vida do inimigo
            health_width = (skeleton.health / skeleton.total_health) * skeleton.rect.width
            current_health_pos = pygame.Rect(pos.x, pos.y - 10, health_width, 5)
            pygame.draw.rect(window, (0, 255, 0), current_health_pos)
        #Desenha a barra de vida do personagem
        draw_player_health(window, 10, 10, playerselected.health / playerselected.total_health)
        pygame.display.update()
    return state

