import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import *
from tilemap import *
# Função para carregar uma imagem e Retorna a imagem carregada
def load_assets():
    assets = {}
    assets['fontinit'] = pygame.font.Font(os.path.join(FNT_DIR,'Bleeding_Cowboys.ttf'), 28)
    assets['boss_font'] = pygame.font.Font(os.path.join(FNT_DIR,'TrashGhostly.ttf'), 40)
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
    assets['attack_lockon'] = []
    img = pygame.image.load(os.path.join(IMG_DIR,'attack_lockon1.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE*2.5, TILESIZE*2.5))
    assets['attack_lockon'].append(img)
    assets['necromancer_attack2_effect'] = []
    for i in range(1,10):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack2_effect0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*2.5, TILESIZE*2.5))
        assets['necromancer_attack2_effect'].append(img)
    assets['necromancer_attack3_effect'] = []
    img = pygame.image.load(os.path.join(ANIM_DIR, 'necromancer', f'necromancer_attack3_effect01.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
    assets['necromancer_attack3_effect'].append(img)


    assets['elite_orc_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_idle'].append(img)
    assets['elite_orc_walk'] = []
    for i in range(1,9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_walk'].append(img)
    assets['elite_orc_attack1'] = []
    for i in range(1,8):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_attack1_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_attack1'].append(img)
    assets['elite_orc_attack2'] = []
    for i in range(1,11):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_attack2_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_attack2'].append(img)
    assets['elite_orc_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_hurt'].append(img)
    assets['elite_orc_death'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'elite_orc', f'elite_orc_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['elite_orc_death'].append(img)


    assets['axeman_idle'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_idle0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_idle'].append(img)
    assets['axeman_walk'] = []
    for i in range(1,7):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_walk'].append(img)
    assets['axeman_attack1'] = []
    for i in range(1,10):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_attack1_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_attack1'].append(img)
    assets['axeman_attack2'] = []
    for i in range(1,12):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_attack2_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_attack2'].append(img)
    assets['axeman_hurt'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_hurt'].append(img)
    assets['axeman_death'] = []
    for i in range(1,5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'axeman', f'axeman_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE*1.5, TILESIZE*1.5))
        assets['axeman_death'].append(img)

    assets['archer_walk'] = []
    for i in range(1, 9):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_walk0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_walk'].append(img)

    assets['archer_hurt'] = []
    for i in range(1, 5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_hurt0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_hurt'].append(img)

    assets['archer_death'] = []
    for i in range(1, 5):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_death0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_death'].append(img)

    assets['archer_attack'] = []
    for i in range(1, 10):
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_attack1_0{i}.png')).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_attack'].append(img)

    assets['archer_special'] = []
    for i in range(1, 13):
        filename = f'archer_attack2_{str(i).zfill(2)}.png'
        img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', filename)).convert_alpha()
        img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
        assets['archer_special'].append(img)

    assets['archer_flecha'] = []
    img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', 'archer_flecha.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE // 2, TILESIZE // 4))
    assets['archer_flecha'].append(img)

    assets['archer_special_arrow'] = []
    img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', 'archer_special_01.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE *1.5, TILESIZE* 1.5))
    assets['archer_special_arrow'].append(img)
    assets['BOSSMUSIC'] = path.join(SND_DIR, 'Soul Of Cinder.wav')  # <- só o caminho

    return assets



    