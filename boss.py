import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spriteszaltron import *
import random
import math


class Necromancer(pygame.sprite.Sprite):
    def __init__(self, x, y, state, player, game_walls, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.animation_frames = self.assets['necromancer_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]

        self.walk_frames = self.assets['necromancer_walk']
        self.current_walk_frame = 0

        self.attack1_frames = self.assets['necromancer_attack1']
        self.current_attack1_frame = 0

        self.attack2_frames = self.assets['necromancer_attack2']
        self.current_attack2_frame = 0

        self.attack3_frames = self.assets['necromancer_attack3']
        self.current_attack3_frame = 0

        self.death_frames = self.assets['necromancer_death']
        self.current_death_frame = 0

        self.collided = False
        self.rect = self.image.get_rect()
        self.hit_rect = BOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = BOSS_HEALTH
        self.total_health = BOSS_HEALTH
        self.last_attack = 0