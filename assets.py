import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import *
from tilemap import Map

def load_assets():
    assets = {}
    assets['fontinit'] = pygame.font.Font(os.path.join(FNT_DIR,'Bleeding_Cowboys.ttf'), 28)
    assets['skeleton_idle'] = []
    for i in range(1,7):
        assets['skeleton_idle'].append(pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_idle0{i}.png')).convert_alpha())
    assets['archer_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_idle'].append(img)
    assets['wizard_idle'] = []   
    for i in range(1,6):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_idle'].append(img)
    assets['map'] = Map(path.join(IMG_DIR, 'map.txt'))
    return assets