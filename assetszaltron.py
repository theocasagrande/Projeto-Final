from assets import load_assets
import pygame
from config import *
import os 

x = load_assets()
x['wizard_attack_ice'] = []
for i in range(1,7):
    img = pygame.image.load(os.path.join(ANIM_DIR, 'wizard', f'Wizard_Attack_ice{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
    x['wizard_attack_ice'].append(img)