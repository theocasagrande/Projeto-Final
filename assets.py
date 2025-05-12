import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import IMG_DIR, FNT_DIR

pygame.font

def load_assets():
    assets = {}
    assets['fontinit'] = pygame.font.Font(os.path.join(FNT_DIR,'Bleeding_Cowboys.ttf'), 28)
    return assets