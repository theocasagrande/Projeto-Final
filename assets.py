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
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_idle'].append(img)
    assets['archer_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_idle'].append(img)
    assets['wizard_idle'] = []   
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_idle'].append(img)
    assets['map'] = Map(path.join(IMG_DIR, 'map2.txt'))
    assets['map_width'] = len(assets['map'].data[0]) * TILESIZE
    assets['map_height'] = len(assets['map'].data) * TILESIZE
    assets['wizard_attack_ice'] = []
    for i in range(1,11):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'Wizard-Attack01_Effect-{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*2.5, TILESIZE*2.5))
        assets['wizard_attack_ice'].append(img)
    assets['wall_tile'] = pygame.image.load(os.path.join(IMG_DIR, 'tile_0014.png')).convert_alpha()
    assets['wizard_attack_ice_anim'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'Wizard-ice_attack_anim-{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.18, TILESIZE))
        assets['wizard_attack_ice_anim'].append(img)
    assets['wizard_walk'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_walk'].append(img)
    assets['wizard_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_hurt0{i}.png')).convert()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_hurt'].append(img)
    return assets