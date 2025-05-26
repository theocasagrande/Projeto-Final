# from assets import load_assets
# import pygame
# from config import *
# import os 
# import assets

#     assets['archer_walk'] = []
#     for i in range(1, 9):
#         img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_walk0{i}.png')).convert_alpha()
#         img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
#         assets['archer_walk'].append(img)

#     assets['archer_hurt'] = []
#     for i in range(1, 5):
#         img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_hurt0{i}.png')).convert_alpha()
#         img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
#         assets['archer_hurt'].append(img)

#     assets['archer_death'] = []
#     for i in range(1, 5):
#         img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_death0{i}.png')).convert_alpha()
#         img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
#         assets['archer_death'].append(img)

#     assets['archer_attack'] = []
#     for i in range(1, 10):
#         img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_attack1_0{i}.png')).convert_alpha()
#         img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
#         assets['archer_attack'].append(img)

#     assets['archer_special'] = []
#     for i in range(1, 13):
#         img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', f'archer_attack2_0{i}.png')).convert_alpha()
#         img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
#         assets['archer_special'].append(img)

#     assets['archer_flecha'] = []
#     img = pygame.image.load(os.path.join(ANIM_DIR, 'archer', 'flecha.png')).convert_alpha()
#     img = pygame.transform.scale(img, (TILESIZE // 2, TILESIZE // 4))
#     assets['archer_flecha'].append(img)