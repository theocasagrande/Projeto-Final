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
    for i in range(1,14):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_special_effect{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_special_effect'].append(img)
    assets['knight_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightidle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['knight_idle'].append(img)
    
    assets['knight_walk'] = []
    for i in range(1, 8):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightwalk01{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['knight_walk'].append(img)
    

    assets['knight_attack'] = []
    for i in range(1, 7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['knight_attack'].append(img)
    assets['knight_special'] = []
    for i in range(1, 12):
        if i < 2:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        elif i < 5:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE // 1.25, TILESIZE))
        elif i < 6 :
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        elif i < 8:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE*1.7, TILESIZE*1.25))

        elif i < 11:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE*2.2, TILESIZE*1.5))
        else:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knightat2{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['knight_special'].append(img)
    assets['wizard_speed_boost'] = []    
    for i in range(1,11):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'wizard_speed_boost{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['wizard_speed_boost'].append(img)
    assets['knight_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'knight', f'knight_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['knight_hurt'].append(img)
    assets['skeleton_death'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_death'].append(img)
    assets['skeleton_archer_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', f'skeleton_archer_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_archer_idle'].append(img)
    assets['skeleton_archer_walk'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', f'skeleton_archer_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_archer_walk'].append(img)
    assets['skeleton_archer_attack'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', f'skeleton_archer_attack0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_archer_attack'].append(img)
    assets['skeleton_archer_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', f'skeleton_archer_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_archer_idle'].append(img)
    assets['skeleton_archer_death'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', f'skeleton_archer_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_archer_death'].append(img)
    assets['skeleton_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', f'skeleton_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['skeleton_hurt'].append(img)
    assets['skeleton_archer_arrow'] = []
    img = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton_archer', 'skeleton_archer_arrow.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE // 2, TILESIZE // 2))
    assets['skeleton_archer_arrow'].append(img)

    assets['necromancer_idle'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_idle'].append(img)
    assets['necromancer_walk'] = []
    for i in range(1,8):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_walk'].append(img)
    assets['necromancer_death'] = []
    for i in range(1,10):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_death'].append(img)
    assets['necromancer_attack1'] = []
    for i in range(1,13):
        if i >= 9:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack1_0{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE*6, TILESIZE*6))
        else:
            img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack1_0{i}.png')).convert_alpha()
            img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_attack1'].append(img)
    assets['necromancer_attack2'] = []
    for i in range(1,14):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack2_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_attack2'].append(img)
    assets['necromancer_attack3'] = []
    for i in range(1,18):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack3_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_attack3'].append(img)
    assets['necromancer_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*4, TILESIZE*4))
        assets['necromancer_hurt'].append(img)
    assets['bossroom'] = TiledMap(path.join(MAP_DIR, 'bossroom.tmx'), SCALE)  # 16 * 4 = 64
    assets['bossroom_surface'] = assets['bossroom'].make_map()
    assets['bossroom_rect'] = assets['bossroom_surface'].get_rect()
    assets['bossroom_width'] = assets['bossroom'].width
    assets['bossroom_height'] = assets['bossroom'].height
    

    return assets


    