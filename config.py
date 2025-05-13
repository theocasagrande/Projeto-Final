from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')
ANIM_DIR = path.join(path.dirname(__file__), 'assets', 'anim')
# Estabelece a pasta que contem os arquivos de configuração.
# Dados gerais do jogo.
WIDTH = 1280  # Largura da tela
HEIGHT = 720 # Altura da tela
FPS = 45 # Frames por segundo

LIGHTGRAY = (200, 200, 200)

INIT = 3
GAME = 1
QUIT = 2

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE