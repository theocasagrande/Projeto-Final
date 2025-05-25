from os import path
import pygame

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')
ANIM_DIR = path.join(path.dirname(__file__), 'assets', 'anim')
MAP_DIR = path.join(path.dirname(__file__), 'assets', 'maps')
# Estabelece a pasta que contem os arquivos de configuração.
# Dados gerais do jogo.
WIDTH = 1280  # Largura da tela 80 grids
HEIGHT = 720 # Altura da tela 45 grids
FPS = 60 # Frames por segundo

LIGHTGRAY = (200, 200, 200)

SCALE = 4

BOSS = 5
INIT = 3
GAME = 1
QUIT = 2

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

YELLOW  = (255,255,0)
MOB_SPEED = 50 * TILESIZE
AVOID_RADIUS = 100
MOB_HIT_RECT = pygame.Rect(0, 0, 64, 64)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
SKELETON_HEALTH = 100
SKELETON_ARCHER_HEALTH = 80
SKELETON_ARCHER_ARROW_RECT = pygame.Rect(0,0,50,50)
ARROW_SPEED = 250
SKELETON_ARCHER_ARROW_DAMAGE = 20

#player stats
PLAYER_SPEED = 200
WIZARD_HEALTH = 100
KNIGHT_HEALTH = 225
ARCHER_HEALTH = 180
PLAYER_HIT_RECT = pygame.Rect(0,0,64,64)
WIZARD_LAYER = 2
SPEEDBOOST_LAYER = 1



KNIGHT_ATTACK_DMG = 50
ICE_ATTACK_DMG = 20
WIZARD_SPECIAL_DMG = 50
KNIGHT_SPECIAL_DMG = 100
ICE_ATTACK_RECT  = pygame.Rect(0,0,80,80)
WIZARD_SPECIAL_RECT = pygame.Rect(0,0,64,64)
KNIGHT_HITBOX_RECT = pygame.Rect(0,0,70,70)
KNIGHT_SPECIAL_HITBOX_RECT = pygame.Rect(0,0, 150,150)


#BOSS STATS

BOSS_HIT_RECT = pygame.Rect(0,0,TILESIZE * 4, TILESIZE*4)
BOSS_HEALTH = 2000
BOSS_SPEED = 15*TILESIZE
NECRO_ATTACK2_HITRECT = pygame.Rect(0,0,TILESIZE*2.5, TILESIZE*2.5)
NECRO_ATTACK2_DMG = 35
NECRO_ATTACK3_HIT_RECT = pygame.Rect(0,0, TILESIZE*1.5, TILESIZE*1.5)
NECRO_ATTACK3_DMG = 20
NECRO_ATTACK3_SPEED = 250