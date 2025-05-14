import pygame
import os
from config import *
from assets import load_assets

class Archer (pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls):
        pygame.sprite.Sprite.__init__(self)
        self.groups = all_sprites
        self.game_walls = game_walls
        self.assets = load_assets()
        self.x = x *TILESIZE
        self.y = y * TILESIZE
        self.state = state
        self.image = self.assets['archer_idle'][0]
        self.animation_frames = self.assets['archer_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.rect = self.image.get_rect()

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
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vy =  PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if self.vx != 0 or self.vy != 0:
            self.state = 'idle'
            
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

class Wizard_attack_ice(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, center, direction):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.image = assets["wizard_attack_ice"][0]
        self.animation_frames = self.assets['wizard_attack_ice']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.rect = self.image.get_rect()
        self.center = center
        self.direction = direction
    
    def update(self):
        # Atualiza a animação
        if self.direction == 'right':
            self.center = (self.center[0] + 5, self.center[1])
        elif self.direction == 'left':
            self.center = (self.center[0] - 5, self.center[1])
        elif self.direction == 'up':
            self.center = (self.center[0], self.center[1] - 5)
        elif self.direction == 'down':
            self.center = (self.center[0], self.center[1] + 5)
        elif self.direction == 'up_right':
            self.center = (self.center[0] + 5, self.center[1] - 5)
        elif self.direction == 'up_left':
            self.center = (self.center[0] - 5, self.center[1] - 5)
        elif self.direction == 'down_right':
            self.center = (self.center[0] + 5, self.center[1] + 5)
        elif self.direction == 'down_left':
            self.center = (self.center[0] - 5, self.center[1] + 5)


        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.animation_frames):
                self.kill()
            else:
                self.image = self.animation_frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.center

                    
