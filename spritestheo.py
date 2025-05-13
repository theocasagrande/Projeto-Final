import pygame
import os
from config import *
from assets import load_assets
from game_screen import *

        
class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, state):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.state = state
        self.animation_frames = self.assets['skeleton_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls):
        pygame.sprite.Sprite.__init__(self)
        self.groups = all_sprites
        self.game_walls = game_walls
        self.assets = load_assets()
        self.dx = 0
        self.dy = 0
        self.x = x 
        self.y = y 
        self.state = state
        self.image = self.assets['wizard_idle'][0]
        self.animation_frames = self.assets['wizard_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
    def collision(self, dx=0, dy=0):
        for wall in self.game_walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    def move(self, dx=0, dy=0):
        if not self.collision(dx, dy):
            self.x += dx
            self.y += dy
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE
        else:
            self.state = 'idle'
            self.dx = 0
            self.dy = 0
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        if self.state == 'idle':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.animation_frames):
                    self.current_frame = 0
                self.image = self.animation_frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
    
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 255, 0))  # Cor preta para a parede
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE