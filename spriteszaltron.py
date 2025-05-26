import pygame
import os
from config import *
from assets import load_assets
from spritestheo import *
import random
vec = pygame.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)
def collision(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            sprite.pos.x = sprite.hit_rect.centerx

    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            sprite.pos.y = sprite.hit_rect.centery
def distance_to(sprite1, sprite2):
    dx = sprite2.rect.centerx - sprite1.rect.centerx
    dy = sprite2.rect.centery - sprite1.rect.centery
    return (dx**2 + dy**2) ** 0.5
def distance_to_group(sprite, group):
    smallestdistance = 10000
    if len(group) != 0:
        for enemy in group:
            distance = distance_to(sprite, enemy)
            if distance <= smallestdistance:
                smallestdistance = distance
                target = enemy
        return smallestdistance, target
    else:
        return smallestdistance, None
    


class Archer (pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.game_walls = game_walls
        self.all_sprites = all_sprites
        self.assets = load_assets()
        self.all_skeletons = all_skeletons
        self.all_projectiles = all_projectiles

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.state = state
        self.frame_rate = 100

        self.original_frames = self.assets['archer_idle']  
        self.animation_frames = list(self.original_frames)

        self.attack1_frames = self.assets['attack1']
        self.original_attack1_frames = list(self.attack1_frames)

        self.hurt_frames = self.assets['archer_hurt']
        self.original_hurt_frames = list(self.hurt_frames)

        self.special_frames = self.assets['attack2']
        self.original_special_frames = list(self.special_frames)

        self.current_frame = 0
        self.current_frameiceattack = 0
        self.current_hurt_frame = 0
        self.current_special_frame = 0

        self.hurt_duration = len(self.hurt_frames) * self.frame_rate
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos 
        self.iceticks = 1000
        self.specialticks = 15000
        self.last_ice_attack = pygame.time.get_ticks()
        self.last_special = pygame.time.get_ticks()
        self.direction = 'right'
        self.prev_direction = None
        self.last_update = pygame.time.get_ticks()
        self.original_walk_frames = self.assets['archer_walk']
        self.walk_frames = list(self.original_walk_frames)
        self.current_framewalk = 0
        self.health = ARCHER_HEALTH
        self.last_hit_time = 0
        self.last_speed = 0
        self.playerspeed = PLAYER_SPEED
        self.speedboost_cooldown = 8000
        self._layer = WIZARD_LAYER
        all_sprites.add(self, layer=self._layer)

    # def collision(self, direction):
    #     hits = pygame.sprite.spritecollide(self, self.game_walls, False)
    #     if hits:
    #         if direction == 'x':
    #             if self.vx > 0:
    #                 self.x = hits[0].rect.left - self.rect.width
    #             elif self.vx < 0:
    #                 self.x = hits[0].rect.right
    #             self.vx = 0
    #             self.rect.x = self.x
    #         elif direction == 'y':
    #             if self.vy > 0:
    #                 self.y = hits[0].rect.top - self.rect.height
    #             elif self.vy < 0:
    #                 self.y = hits[0].rect.bottom
    #             self.vy = 0
    #             self.rect.y = self.y


    

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if self.state != 'archer_hurt':
            if keys[pygame.K_SPACE]:
                if now - self.last_ice_attack > self.iceticks:
                    self.state = 'attack1'
                    self.attack1()
                    self.last_ice_attack = pygame.time.get_ticks()
            elif keys[pygame.K_f]:
                if now - self.last_special > self.specialticks:
                    self.state = 'attack2'
                    self.last_special = pygame.time.get_ticks()

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, -1)
            self.direction = 'up_left'
            if self.state not in ('attack1', 'archer_hurt', 'attack2'):
                self.state = 'walk'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, -1)
            self.direction = 'up_right'
            if self.state not in ('attack1', 'archer_hurt', 'attack2'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, 1)
            self.direction = 'down_left'
            if self.state not in ('attack1', 'archer_hurt', 'attack2'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, 1)
            self.direction = 'down_right'
            if self.state not in ('attack1', 'archer_hurt', 'attack2'):
                self.state = 'walk'
        else:
            if keys[pygame.K_LEFT]:
                self.vel.x = -1
                self.direction = 'left'
                if self.state not in ('archer_attack', 'archer_hurt', 'attack2'):

                    self.state = 'walk'
            if keys[pygame.K_RIGHT]:
                self.vel.x = 1
                self.direction = 'right'
                if self.state not in ('archer_attack', 'archer_hurt', 'attack2'):

                    self.state = 'walk'
            if keys[pygame.K_UP]:
                self.vel.y = -1
                self.direction = 'up'
                if self.state not in ('archer_attack', 'archer_hurt', 'attack2'):

                    self.state = 'walk'
            if keys[pygame.K_DOWN]:
                self.vel.y = 1
                self.direction = 'down'
                if self.state not in ('archer_attack', 'archer_hurt', 'attack2'):

                    self.state = 'walk'
                
        if self.vel.length() != 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
        else:
            if self.state not in ('archer_attack', 'archer_hurt', 'attack2'):

                self.state = 'idle'
            self.vel = vec(0, 0)
            
    def update(self, dt):
        self.get_keys()
        
        if self.direction != self.prev_direction:
            self.rotate_image(self.direction)
            self.prev_direction = self.direction

        now = pygame.time.get_ticks()
        
  
        if self.state == 'attack1':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frameiceattack += 1
                if self.current_frameiceattack >= len(self.ice_attack_frames):
                    self.state = 'archer_idle'
                    self.current_frameiceattack = 0
                self.image = self.ice_attack_frames[self.current_frameiceattack]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center

        if self.state in ('attack2', 'speed'):

            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_special_frame += 1
                if self.current_special_frame >= len(self.special_frames):
                    self.state = 'archer_idle'
                    self.current_special_frame = 0
                self.image = self.special_frames[self.current_special_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center

        if self.state == 'archer_hurt':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_hurt_frame += 1
                if self.current_hurt_frame >= len(self.hurt_frames):
                    self.state = 'archer_idle'
                    self.current_hurt_frame = 0
                self.image = self.hurt_frames[self.current_hurt_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center
        
        

        if self.state not in ('attack1', 'archer_hurt', 'attack2'):
          
            if self.state == 'archer_walk':
                frames = self.walk_frames
                current_frame = self.current_framewalk
            else: 
                frames = self.animation_frames
                current_frame = self.current_frame

   
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                current_frame = (current_frame + 1) % len(frames)
                self.image = frames[current_frame]
                
    
                if self.state == 'archer_walk':
                    self.current_framewalk = current_frame
                else:
                    self.current_frame = current_frame
                
 
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center


      
        self.rect.center = self.pos
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center

        now2 = pygame.time.get_ticks()
        if now2 - self.last_speed >= self.speedboost_cooldown:
            self.playerspeed = PLAYER_SPEED



    def rotate_image(self, direction):

        flip = direction in ['left', 'up_left', 'down_left']
        
        self.animation_frames = [
            pygame.transform.flip(img, flip, False) 
            for img in self.original_frames
        ]
        
        self.walk_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_walk_frames
        ]
        
        self.ice_attack_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_attack1_frames
        ]

        self.hurt_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_hurt_frames
        ]
        
        self.special_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_special_frames
        ]
        
 
        if self.state == 'archer_walk':
            self.image = self.walk_frames[self.current_framewalk]
        elif self.state == 'attack1':
            self.image = self.ice_attack_frames[self.current_frameiceattack]
        elif self.state == 'archer_hurt':
            self.image = self.hurt_frames[self.current_hurt_frame]
        elif self.state == 'attack2':
            self.image = self.special_frames[self.current_special_frame]
        else:
            self.image = self.animation_frames[self.current_frame]
      
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.hit_rect.center = self.rect.center




    def attack1(self):
            attack1 = archer_attack1(self,self.pos, self.direction, self.all_skeletons, self.assets)
            self.all_sprites.add(attack1)
            self.all_projectiles.add(attack1)
    
    # def attack2(self):
    #     attack2 = archer_attack2(self, self.rect.center, self.all_skeletons, self.assets)
    #     self.all_sprites.add(attack2)
    #     self.all_projectiles.add(attack2)
    #     self.last_special = pygame.time.get_ticks()

        

class archer_attack1 (pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player, center, direction, all_skeletons, assets):
        pygame.sprite.Sprite.__init__(self)
        self.all_skeletons = all_skeletons
        self.player = player
        self.image = assets['archer_flecha'][0]
        self.rect = self.image.get_rect()
        self.hit_rect = ICE_ATTACK_RECT.copy()
        self.damaged_enemies = set()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    
       
        offset = 5 * TILESIZE
        cx, cy = center
        distance, target = distance_to_group(self.player, all_skeletons)

        if target and distance <= 5*TILESIZE:
            self.rect.center = target.rect.center
        else:
            
            offset = vec(0, 0)
            if direction == 'right':
                offset = vec(5*TILESIZE, 0)
            elif direction == 'left':
                offset = vec(-5*TILESIZE, 0)
            elif direction == 'up':
                offset = vec(0, -5*TILESIZE)
            elif direction == 'down':
                offset = vec(0, 5*TILESIZE)
            elif direction == 'up_right':
                offset = vec(4*TILESIZE, -4*TILESIZE)  # Diagonal
            elif direction == 'up_left':
                offset = vec(-4*TILESIZE, -4*TILESIZE)
            elif direction == 'down_right':
                offset = vec(4*TILESIZE, 4*TILESIZE)
            elif direction == 'down_left':
                offset = vec(-4*TILESIZE, 4*TILESIZE)
            
            self.rect.center = (center[0] + offset.x, center[1] + offset.y)

                

