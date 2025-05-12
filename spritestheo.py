import pygame
import os
from config import *
from assets import load_assets


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ANIM_DIR, 'skeleton', 'skeleton_idle01.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_frames = []
        self.state = state
        self.assets = load_assets()
    def load_idle_animation(self):
            self.animation_frames = self.assets['skeleton_idle'][:]
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100
            while self.current_frame < len(self.animation_frames):
                now = pygame.time.get_ticks()
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    self.image = self.animation_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.rect.x
                    self.current_frame += 1
                    if self.current_frame > len(self.animation_frames):
                        self.current_frame = 0
                    
    def update(self):
        if self.state == 'idle':
            self.load_idle_animation()
        elif self.state == 'attack':
            self.load_attack_animation()
        elif self.state == 'die':
            self.load_die_animation()
        else:
            raise ValueError("Invalid state")