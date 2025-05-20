import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spritestheo import distance_to, collision   
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
        self.iwalk_frames = self.assets['knight_walk']
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

    def load_knight_img(self, name):
        path_img = os.path.join("assersBruno", name + ".png")
        img = pygame.image.load(path_img).convert_alpha()
        return pygame.transform.scale(img, (TILESIZE, TILESIZE))

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

        if keys[pygame.K_LEFT]:
            self.vel.x = -1
            self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.vel.x = 1
            self.direction = 'right'
        if keys[pygame.K_UP]:
            self.vel.y = -1
            self.direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.vel.y = 1
            self.direction = 'down'

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
                            self.damage_nearby_enemies(ICE_ATTACK_DMG)
                else:
                    self.state = 'idle'

            elif self.state == 'special':
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    if self.current_special_frame < len(self.special_frames):
                        self.image = self.special_frames[self.current_special_frame]
                        self.current_special_frame += 1
                        if self.current_special_frame == 5:
                            self.damage_nearby_enemies(ICE_ATTACK_DMG * 2)
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

        def damage_nearby_enemies(self, dmg):
            for skeleton in self.all_skeletons:
                if distance_to(self, skeleton) <= TILESIZE * 1.5:
                    skeleton.health -= dmg



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


