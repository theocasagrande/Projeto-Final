import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spriteszaltron import *

dt = FPS / 1000
vec = pygame.math.Vector2
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
            pygame.sprite.Sprite.__init__(self, all_sprites)
            self.game_walls = game_walls
            self.all_sprites = all_sprites
            self.assets = load_assets()

            self.vel = vec(0, 0)
            self.pos = vec(x * TILESIZE, y * TILESIZE)
            self.state = state

            self.original_frames = self.assets['wizard_idle']
            self.animation_frames = list(self.original_frames)
            self.current_frame = 0
            self.image = self.animation_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.pos 
            self.iceticks = 1000
            self.last_ice_attack = pygame.time.get_ticks()
            self.direction = 'right'
            self.prev_direction = None
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100





    def collision(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game_walls, False)
        if hits:
            if direction == 'x':
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x
            elif direction == 'y':
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height / 2
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height / 2
                self.vel.y = 0
                self.rect.centery = self.pos.y

    

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()

        # Handle diagonals first
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, -1)
            self.direction = 'up_left'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, -1)
            self.direction = 'up_right'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, 1)
            self.direction = 'down_left'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, 1)
            self.direction = 'down_right'
        else:
            if keys[pygame.K_LEFT]:
                self.vel.x = -1
                self.direction = 'left'
            if keys[pygame.K_RIGHT]:
                self.vel.x = 1
                self.direction = 'right'
            if keys[pygame.K_UP]:
                self.vel.y = -1
                self.direction = 'up'
            if keys[pygame.K_DOWN]:
                self.vel.y = 1
                self.direction = 'down'

        # Normalize for diagonal movement
        if self.vel.length() != 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
            self.state = 'idle'

        if keys[pygame.K_SPACE]:
            self.ice_attack()


            
    def update(self, dt):
        self.get_keys()

        # Only flip if direction changed
        if self.direction != self.prev_direction:
            self.rotate_image(self.direction)
            self.prev_direction = self.direction

        # Set current frame image
        self.image = self.animation_frames[self.current_frame]

        # Position and collisions
        self.pos.x += self.vel.x * dt
        self.rect.centerx = self.pos.x
        self.collision('x')

        self.pos.y += self.vel.y * dt
        self.rect.centery = self.pos.y
        self.collision('y')

        # Animation update
        if self.state == 'idle':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center


    def ice_attack(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_ice_attack
        if elapsed_ticks > self.iceticks:
            self.last_ice_attack = now
            ice_attack = Wizard_attack_ice(self.assets,self.pos, self.direction)
            self.all_sprites.add(ice_attack) 
    def rotate_image(self, direction):
        if direction == 'left' or direction == 'up_left' or direction == 'down_left':
            self.animation_frames = [pygame.transform.flip(img, True, False) for img in self.original_frames]
        elif direction == 'right' or direction == 'up_right' or direction == 'down_right':
            self.animation_frames = list(self.original_frames)

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


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)