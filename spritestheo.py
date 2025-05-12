import pygame
import os
from config import *
from assets import load_assets
        
class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, state):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.state = state

        # Carrega os frames da animação idle
        self.animation_frames = self.assets['skeleton_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # ms entre frames

        # Define a imagem inicial e a posição
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        if self.state == 'idle':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.animation_frames):
                    self.current_frame = 0
                self.image = self.animation_frames[self.current_frame]
                

                # Preserva a posição
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center