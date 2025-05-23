# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import *
from assets import load_assets
import time
import os
from os import path
from init_screen import init_screen
from game_screen import game_screen
from boss_room import boss_room

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soul Knightmare")


state = INIT
while state != QUIT:
    if state == INIT:
        state, player = init_screen(window)
    elif state == GAME:
        state, player = game_screen(window, player)
    elif state == BOSS:
        state = boss_room(window,player)
    else:
        state = QUIT

pygame.quit()