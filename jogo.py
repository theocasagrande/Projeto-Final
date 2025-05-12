# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, IMG_DIR, INIT, GAME, QUIT
from assets import load_assets
import time
import os
from os import path
from init_screen import init_screen
from game_screen import game_screen

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soul Knightmare")


state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window)
    else:
        state = QUIT

pygame.quit()