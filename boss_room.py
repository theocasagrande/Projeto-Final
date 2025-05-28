import pygame
import random
from os import path
from config import *
from assets import load_assets
import time
from sprites import *
# ----- Cores
vec = pygame.math.Vector2

#Desenha a barra de vida do boss e nome
def draw_boss_health(surface, x, y, width, height, pct, font, boss_name):
    if pct < 0:
        pct = 0
    # Fundo da barra (vermelho)
    outline_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (255, 0, 0), outline_rect)
    # Barra preenchida (verde)
    fill_width = int(pct * width)
    fill_rect = pygame.Rect(x, y, fill_width, height)
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)
    # Contorno branco
    pygame.draw.rect(surface, (139, 0 , 0), outline_rect, 3)

    # Renderiza o nome do boss acima da barra, com sombra para melhorar a visibilidade
    text_surface = font.render(boss_name, True, (230, 0, 0))
    shadow_surface = font.render(boss_name, True, (0, 0, 0))

    # Ajuste a posição do texto - um pouco acima da barra
    text_rect = text_surface.get_rect(midbottom=(x + width // 2, y + 80))

    # Desenha sombra (offset de 2 pixels para direita e baixo)
    surface.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
    # Desenha texto branco em cima
    surface.blit(text_surface, text_rect)

# Desenha a barra de vida do player
def draw_player_health(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    #Criação do rect do outline
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    #Criação do rect da barra de vida
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    if pct > 0.6:
        # Se o personagem tiver mais de 60% de sua vida total, a barra tem cor verde
        col = (0, 255, 0)
    elif pct > 0.3:
        # Se o personagem tiver entre 30% e 60% de sua vida total, a barra tem cor amarela
        col = (255, 255, 0)
    else:
        # Se o personagem tiver menos de 30% de vida, a barra tem cor vermelha
        col = (255, 0, 0)

    #Desenha a barra de vida
    pygame.draw.rect(surface, col, fill_rect)
    pygame.draw.rect(surface, (255,255,255), outline_rect, 2)
def boss_room(window, player):
    # ----- Inicia o jogo
    pygame.init()
    pygame.mixer.init()
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

    

# Criação do jogador e paredes
# Faz leitura do arquivo tmx. do mapa e posiciona cada sprite de acordo com a posição dos objetos na layer de objetos no mapa.
    for tile_object in assets['bossroom'].tmxdata.objects:
        if tile_object.name == 'player':
            if player == 'knight':
                playerselected = Knight(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
                playerselected.rect.center = (tile_object.x * SCALE, tile_object.y * SCALE)
                playerselected.hit_rect.center = playerselected.rect.center

            elif player == 'wizard':
                playerselected = Wizard(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
                playerselected.rect.center = (tile_object.x * SCALE, tile_object.y * SCALE)
                playerselected.hit_rect.center = playerselected.rect.center

            elif player == 'archer':
                playerselected = Archer(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                                        all_sprites, game_walls, all_skeletons, all_projectiles)
                playerselected.rect.center = (tile_object.x * SCALE, tile_object.y * SCALE)
                playerselected.hit_rect.center = playerselected.rect.center

        elif tile_object.name == 'wall':
            wall = Obstacle(tile_object.x * SCALE, tile_object.y * SCALE,
                            tile_object.width * SCALE, tile_object.height * SCALE)
            all_sprites.add(wall)
            game_walls.add(wall)

    # Cria e posiciona o boss
    for tile_object in assets['bossroom'].tmxdata.objects:
        if tile_object.name == 'boss_spawn' and playerselected is not None:
            boss = Necromancer(tile_object.x * SCALE, tile_object.y * SCALE, 'idle',
                            playerselected, game_walls, all_skeletons, assets, enemy_projectiles)
            all_sprites.add(boss)
            all_skeletons.add(boss)

    playerselected.health = playerselected.total_health
            
    
    # Cria a camera do jogo
    camera = Camera(assets['bossroom_width'], assets['bossroom_height'])
    # Posiciona a camera do jogo no jogador
    camera.update(playerselected)

    all_sprites.add(all_skeletons)
    all_sprites.add(all_projectiles)
    all_sprites.add(enemy_projectiles)
    
    #Música de fundo
    pygame.mixer.music.load(assets['BOSSMUSIC'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)  


    while state != DONE:

        dt = clock.tick(FPS) / 1000  # seconds
        pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))
        # Fecha o jogo se apertar ESC ou o X na aba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = DONE
        # Atualiza o estado dos sprites
        for sprite in all_sprites:
            if isinstance(sprite, (Wizard, Knight, Archer, Skeleton, SkeletonArcher, SkeletonArcherArrow, NecromancerAttack3, Archer,
                        Arrow, ArrowSpecial, Necromancer)):
                sprite.update(dt)
            elif isinstance(sprite, Obstacle):
                continue
            elif isinstance(sprite, BossRoomTeleport):
                continue
            else:
                sprite.update()
        # Atualiza posição da camera
        camera.update(playerselected)
        now = pygame.time.get_ticks()
    
        # Verifica colisão entre personagem e inimigo e aplica dano no personagem
        selfhits = pygame.sprite.spritecollide(playerselected, all_skeletons, False, collide_hit_rect)
        if selfhits:
            for hit in selfhits:
                if not isinstance(hit, Necromancer):  # Evita dano do próprio boss
                    if now - playerselected.last_hit_time > 1000:  # 1000 ms = 1 segundo
                        playerselected.health -= MOB_DAMAGE
                        hit.vel = vec(0, 0)
                        playerselected.state = 'hurt'
                        playerselected.last_hit_time = now  # Atualiza o tempo do último hit
        # Se vida do jogador acabar, muda a cena para a tela de tentar de novo
        if playerselected.health <= 0:
            return RETRY, playerselected, True
        
        # Desenha os sprites
        window.blit(assets['bossroom_surface'], camera.apply_rect(assets['bossroom_rect']))
        for sprite in all_sprites:
            window.blit(sprite.image, camera.apply(sprite))
            # Para o jogo quando o boss morre e muda a tela para a tela de vencedor
            if isinstance(sprite, Necromancer):
                if sprite.state == 'death':
                    pygame.mixer.music.stop()
                    if sprite.death_animation_complete:
                        return WINNER, playerselected, True
        # Desenha a barra de vida dos inimigos
        for skeleton in all_skeletons:
            if not isinstance(skeleton, Necromancer):
                # Calcula posição da barra de vida em relação à camera
                pos = camera.apply(skeleton)
                health_pos = pygame.Rect(pos.x, pos.y - 10, skeleton.rect.width, 5)
                
                # Desenha o background da barra de vida (vermelha)
                pygame.draw.rect(window, (255, 0, 0), health_pos)
                
                # Desenha a barra de vida variando seu tamanho de acordo com a vida do boss
                health_width = (skeleton.health / skeleton.total_health) * skeleton.rect.width
                current_health_pos = pygame.Rect(pos.x, pos.y - 10, health_width, 5)
                pygame.draw.rect(window, (0, 255, 0), current_health_pos)


        draw_player_health(window, 10, 10, playerselected.health / playerselected.total_health)
        # Desenha o nome do boss e a barra de vida
        draw_boss_health(window, WIDTH // 2 - 300, 20, 600, 40, boss.health / boss.total_health, assets['boss_font'], "Thanatos, O Invocador de Cadaveres")
        pygame.display.update()
    return state, playerselected