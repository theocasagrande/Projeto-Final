import pygame
import os
from config import *
from assets import load_assets
from game_screen import *

dt = FPS / 1000
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
        self.x = x *TILESIZE
        self.y = y * TILESIZE
        self.state = state
        self.image = self.assets['wizard_idle'][0]
        self.animation_frames = self.assets['wizard_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.rect = self.image.get_rect()
        self.direction = 0


    def collision(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game_walls, False)
        if hits:
            if direction == 'x':
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                elif self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            elif direction == 'y':
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                elif self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
            self.direction = 'left'
        if keys[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
            self.direction = 'up'
        if keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
            self.direction = 'right'
        if keys[pygame.K_DOWN]:
            self.vy =  PLAYER_SPEED
            self.direction = 'down'
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if self.vx != 0 or self.vy != 0:
            self.state = 'idle'
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.direction = 'up_left'
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.direction = 'up_right'
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.direction = 'down_left'
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.direction = 'down_right' 
            
    def update(self, dt):
        self.get_keys()
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.x = self.x
        self.collision('x')
        self.rect.y = self.y
        self.collision('y')
        if pygame.sprite.spritecollideany(self, self.game_walls):
            self.x -= self.vx * dt
            self.y -= self.vy * dt



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