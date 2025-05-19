import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import *
from tilemap import *

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
    assets['map'] = TiledMap(path.join(MAP_DIR, 'dungeonmap1.tmx'), SCALE)  # 16 * 4 = 64
    assets['map_surface'] = assets['map'].make_map()
    assets['map_rect'] = assets['map_surface'].get_rect()
    assets['map_width'] = assets['map'].width
    assets['map_height'] = assets['map'].height
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
    assets['skeleton_walk'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_walk'].append(img)
    assets['skeleton_attack'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_attack0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_attack'].append(img)
    assets['wizard_special'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_special0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_special'].append(img)
    assets['wizard_special_effect'] = []
    for i in range(1,11):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_special_effect{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_special_effect'].append(img)
    return assets