from os import path
import pygame

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')
ANIM_DIR = path.join(path.dirname(__file__), 'assets', 'anim')
# Estabelece a pasta que contem os arquivos de configuração.
# Dados gerais do jogo.
WIDTH = 1280  # Largura da tela 80 grids
HEIGHT = 720 # Altura da tela 45 grids
FPS = 60 # Frames por segundo

LIGHTGRAY = (200, 200, 200)

INIT = 3
GAME = 1
QUIT = 2

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

YELLOW  = (255,255,0)
MOB_SPEED = 10*TILESIZE
MOB_HIT_RECT = pygame.Rect(0, 0, 30, 30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 40

#player stats
PLAYER_SPEED = 200
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = pygame.Rect(0,0,64,64)

ICE_ATTACK_DMG = 20
ICE_ATTACK_RECT  = pygame.Rect(0,0,64,64)