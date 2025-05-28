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
from retry import retry_screen
from end import winner_screen

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption("Soul Knightmare")


state = INIT
while state != QUIT:
    if state == INIT:
        state, player = init_screen(window)
    elif state == GAME:
        state, player, enteredbossroom = game_screen(window, player)
    elif state == BOSS:
        state, player, enteredbossroom = boss_room(window,player)
    elif state == RETRY:
        state, player = retry_screen(window, player, enteredbossroom)
    elif state == WINNER:
        state, player, enteredbossroom = winner_screen(window, player, enteredbossroom)
    else:
        state = QUIT

pygame.quit()