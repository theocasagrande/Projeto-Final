import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spritestheo import distance_to, collision, collide_hit_rect
vec = pygame.math.Vector2
class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.game_walls = game_walls
        self.all_sprites = all_sprites
        self.all_skeletons = all_skeletons

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.state = state
        self.frame_rate = 100
        self.direction = 'right'
        self.prev_direction = None
        self.last_update = pygame.time.get_ticks()

        self.idle_frames = self.assets['knight_idle']  
        self.walk_frames = self.assets['knight_walk']
        self.attack_frames = self.assets['knight_attack']
        self.special_frames = self.assets['knight_special']
        self.hurt_frames = self.assets['wizard_hurt']

        self.special_frames = self.assets['wizard_special']
        self.original_special_frames = list(self.special_frames)


        self.original_idle = list(self.idle_frames)
        self.original_walk = list(self.walk_frames)
        self.original_attack = list(self.attack_frames)
        self.original_special = list(self.special_frames)

        self.current_frame = 0
        self.current_attack_frame = 0
        self.current_special_frame = 0

        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos

        self.health = PLAYER_HEALTH
        self.attack_cooldown = 800
        self.special_cooldown = 5000
        self.last_attack = 0
        self.last_special = 0
        self.playerspeed = PLAYER_SPEED
        self.damaged_enemies = set()


    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if self.state != 'hurt':
            if keys[pygame.K_SPACE] and now - self.last_attack > self.attack_cooldown:
                self.state = 'attack'
                self.last_attack = now
                self.current_attack_frame = 0
            elif keys[pygame.K_f] and now - self.last_special > self.special_cooldown:
                self.state = 'special'
                self.last_special = now
                self.current_special_frame = 0

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.vel = vec(-self.playerspeed, -self.playerspeed)
            self.direction = 'up_left'
            if self.state not in ('attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.vel = vec(self.playerspeed, -self.playerspeed)
            self.direction = 'up_right'
            if self.state not in ('attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.vel = vec(-self.playerspeed, self.playerspeed)
            self.direction = 'down_left'
            if self.state not in ('attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.vel = vec(self.playerspeed, self.playerspeed)
            self.direction = 'down_right'
            if self.state not in ('attack', 'hurt', 'special'):
                self.state = 'walk'
        else:
            if keys[pygame.K_LEFT]:
                self.vel.x = -self.playerspeed
                self.direction = 'left'
                if self.state not in ('attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_RIGHT]:
                self.vel.x = self.playerspeed
                self.direction = 'right'
                if self.state not in ('attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_UP]:
                self.vel.y = -self.playerspeed
                self.direction = 'up'
                if self.state not in ('attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_DOWN]:
                self.vel.y = self.playerspeed
                self.direction = 'down'
                if self.state not in ('attack', 'hurt', 'special'):
                    self.state = 'walk'

        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
            if self.state not in ('attack', 'special', 'hurt'):
                self.state = 'walk'
        else:
            if self.state not in ('attack', 'special', 'hurt'):
                self.state = 'idle'

    def update(self, dt):
        self.get_keys()
        now = pygame.time.get_ticks()

        if self.state == 'attack':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack_frame < len(self.attack_frames):
                    self.image = self.attack_frames[self.current_attack_frame]
                    self.current_attack_frame += 1
                    if self.current_attack_frame == 3:
                            self.damage_nearby_enemies(KNIGHT_ATTACK_DMG)
                else:
                    self.state = 'idle'

        elif self.state == 'special':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_special_frame < len(self.special_frames):
                    self.image = self.special_frames[self.current_special_frame]
                    self.current_special_frame += 1
                    if self.current_special_frame == 5:
                        self.damage_nearby_enemies(KNIGHT_ATTACK_DMG * 2)
                else:
                    self.state = 'idle'

        elif self.state in ('idle', 'walk'):
                frames = self.idle_frames if self.state == 'idle' else self.walk_frames
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(frames)
                    self.image = frames[self.current_frame]

        
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

    def damage_nearby_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= KNIGHT_ATTACK_DMG
                self.damaged_enemies.add(skeleton)



class Arrow(pygame.sprite.Sprite):
     def __init__(self, x, y, direction, arrow_img):
         pygame.sprite.Sprite.__init__(self)
         self.original_image = arrow_img
         self.image = self.rotate_image(direction)
         self.rect = self.image.get_rect()
         self.rect.center = (x, y)
         self.speed = 100
         self.direction = direction
         self.vx, self.vy = self.get_velocity_vector(direction)
     def rotate_image(self, direction):
         if direction == 'up':
             return pygame.transform.rotate(self.original_image, 0)
         elif direction == 'down':
             return pygame.transform.rotate(self.original_image, 180)
         elif direction == 'left':
             return pygame.transform.rotate(self.original_image, 90)
         elif direction == 'right':
             return pygame.transform.rotate(self.original_image, -90)
         elif direction == 'up_left':
             return pygame.transform.rotate(self.original_image, 45)
         elif direction == 'up_right':
             return pygame.transform.rotate(self.original_image, -45)
         elif direction == 'down_left':
             return pygame.transform.rotate(self.original_image, 135)
         elif direction == 'down_right':
             return pygame.transform.rotate(self.original_image, -135)
     def get_velocity_vector(self, direction):
         if direction == 'up':
             return (0, -1)
         elif direction == 'down':
             return (0, 1)
         elif direction == 'left':
             return (-1, 0)
         elif direction == 'right':
             return (1, 0)
         elif direction == 'up_left':
             return (-0.707, -0.707)
         elif direction == 'up_right':
             return (0.707, -0.707)
         elif direction == 'down_left':
             return (-0.707, 0.707)
         elif direction == 'down_right':
             return (-0.707, -0.707)


