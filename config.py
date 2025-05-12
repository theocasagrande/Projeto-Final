from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
WIDTH = 1920  # Largura da tela
HEIGHT = 1080 # Altura da tela
FPS = 45 # Frames por segundo

INIT = 0
GAME = 1
QUIT = 2