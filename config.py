from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')
ANIM_DIR = path.join(path.dirname(__file__), 'assets', 'anim')
# Estabelece a pasta que contem os arquivos de configuração.
# Dados gerais do jogo.
WIDTH = 1920  # Largura da tela
HEIGHT = 1080 # Altura da tela
FPS = 45 # Frames por segundo

INIT = 3
GAME = 1
QUIT = 2