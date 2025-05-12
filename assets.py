import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import *

pygame.font

def load_assets():
    assets = {}
    assets['fontinit'] = pygame.font.Font(os.path.join(FNT_DIR,'Bleeding_Cowboys.ttf'), 28)
    assets['skeleton_idle'] = []
    for i in range(1,7):
        assets['skeleton_idle'].append(pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_idle0{i}.png')).convert_alpha())
    return assets