import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spritestheo import *
vec = pygame.math.Vector2
class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.game_walls = game_walls
        self.all_sprites = all_sprites
        self.all_skeletons = all_skeletons
        self.all_projectiles = all_projectiles

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.state = state
        self.frame_rate = 100
        self.special_frame_rate = 150
        self.direction = 'right'
        self.prev_direction = None
        self.last_update = pygame.time.get_ticks()

        self.idle_frames = self.assets['knight_idle']  
        self.walk_frames = self.assets['knight_walk']
        self.attack_frames = self.assets['knight_attack']
        self.special_frames = self.assets['knight_special']
        self.hurt_frames = self.assets['knight_hurt']

        self.special_frames = self.assets['knight_special']



        self.original_idle = list(self.idle_frames)
        self.original_walk = list(self.walk_frames)
        self.original_attack = list(self.attack_frames)
        self.original_special = list(self.special_frames)
        self.original_hurt = list(self.hurt_frames)

        self.current_frame = 0
        self.current_attack_frame = 0
        self.current_special_frame = 0
        self.current_walk_frame = 0
        self.current_hurt_frame = 0

        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.original_hit_rect_width = PLAYER_HIT_RECT.width
        self.original_hit_rect_height = PLAYER_HIT_RECT.height
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.original_hit_rect_center = self.hit_rect.center
        self.rect.center = self.pos

        self.health = KNIGHT_HEALTH
        self.total_health = KNIGHT_HEALTH
        self.attack_cooldown = 800
        self.special_cooldown = 5000
        self.last_attack = 0
        self.last_special = 0
        self.last_hit_time = 0
        self.playerspeed = PLAYER_SPEED
        self.damaged_enemies = set()
        self._layer = WIZARD_LAYER
        self.attack_offset = 0
        all_sprites.add(self, layer=self._layer)


    
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if self.state != 'hurt':
            if keys[pygame.K_SPACE] and now - self.last_attack > self.attack_cooldown:
                self.state = 'attack'
                self.last_attack = now
                self.current_attack_frame = 0
                self.attack()
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
    def attack(self):
        hitbox = KnightAttackHitbox(self)
        self.all_sprites.add(hitbox)
    def special(self):
        special = KnightSpecialHitbox(self)
        self.all_sprites.add(special)
        

    def update(self, dt):
        self.get_keys()
        now = pygame.time.get_ticks()

        if self.direction != self.prev_direction:
            self.rotate_image(self.direction)
            self.prev_direction = self.direction

        if self.state == 'attack':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_attack_frame += 1
                if self.current_attack_frame >= len(self.attack_frames):
                    self.state = 'idle'
                    self.current_attack_frame = 0
                self.image = self.attack_frames[self.current_attack_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center
                    

        elif self.state == 'special':
            if now - self.last_update > self.special_frame_rate:
                self.last_update = now
                if self.current_special_frame == 6:
                    self.special()
                if self.current_special_frame < len(self.special_frames):
                    self.image = self.special_frames[self.current_special_frame]
                    self.current_special_frame += 1
                else:
                    self.state = 'idle'
                    self.current_special_frame = 0
        elif self.state == 'hurt':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_hurt_frame += 1
                if self.current_hurt_frame >= len(self.hurt_frames):
                    self.state = 'idle'
                    self.current_hurt_frame = 0
                self.image = self.hurt_frames[self.current_hurt_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center

        if self.state not in ('attack', 'hurt', 'special'):
          
            if self.state == 'walk':
                frames = self.walk_frames
                current_frame = self.current_walk_frame
            else: 
                frames = self.animation_frames
                current_frame = self.current_frame

   
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                current_frame = (current_frame + 1) % len(frames)
                self.image = frames[current_frame]
                
    
                if self.state == 'walk':
                    self.current_walk_frame = current_frame
                else:
                    self.current_frame = current_frame
                
 
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center

        
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

    def rotate_image(self, direction):

        flip = direction in ['left', 'up_left', 'down_left']
        
        self.animation_frames = [
            pygame.transform.flip(img, flip, False) 
            for img in self.original_idle
        ]
        
        self.walk_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_walk
        ]
        
        self.attack_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_attack
        ]

        self.hurt_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_hurt
        ]
        
        self.special_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_special
        ]
        
 
        if self.state == 'walk':
            self.image = self.walk_frames[self.current_walk_frame]
        elif self.state == 'ice_attack':
            self.image = self.attack_frames[self.current_attack_frame]
        elif self.state == 'hurt':
            self.image = self.hurt_frames[self.current_hurt_frame]
        elif self.state == 'special':
            if self.current_special_frame < len(self.special_frames):
                self.image = self.special_frames[self.current_special_frame]
            else:
                self.image = self.special_frames[0] if self.special_frames else self.image
        else:
            self.image = self.animation_frames[self.current_frame]
      
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.hit_rect.center = self.rect.center




class KnightAttackHitbox(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.hit_rect = KNIGHT_HITBOX_RECT.copy()
        self.hit_rect.center = self.player.hit_rect.center
        self.all_skeletons = self.player.all_skeletons
        self.attack_duration = 600 
        self.last_update = pygame.time.get_ticks()
        self.image = pygame.Surface((self.hit_rect.width, self.hit_rect.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.hit_rect.center)
        self.damaged_enemies = set()
        
    def update(self):
        now = pygame.time.get_ticks()
        

        if  self.player.direction in ('up_right', 'right', 'down_right'):
            self.hit_rect.left = self.player.hit_rect.right
        elif  self.player.direction in ('up_left', 'left', 'down_left'):
            self.hit_rect.right = self.player.hit_rect.left
        elif  self.player.direction == 'up':
            self.hit_rect.bottom = self.player.hit_rect.top
        elif  self.player.direction == 'down':
            self.hit_rect.top = self.player.hit_rect.bottom



        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= KNIGHT_ATTACK_DMG
                # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
                if isinstance(skeleton, EliteOrc):
                    if skeleton.state != 'attack2':
                        skeleton.state = 'hurt'
                elif not isinstance(skeleton, Necromancer):
                    skeleton.state = 'hurt'
                self.damaged_enemies.add(skeleton)
        
        if now - self.last_update >= self.attack_duration:
            self.kill()

        self.rect.center = self.hit_rect.center

class KnightSpecialHitbox(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.hit_rect = KNIGHT_SPECIAL_HITBOX_RECT.copy()
        self.hit_rect.center = self.player.hit_rect.center
        self.all_skeletons = self.player.all_skeletons
        self.attack_duration = 500 
        self.last_update = pygame.time.get_ticks()
        self.image = pygame.Surface((self.hit_rect.width, self.hit_rect.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.hit_rect.center)
        self.damaged_enemies = set()


    def update(self):
        now = pygame.time.get_ticks()
        

        if  self.player.direction in ('up_right', 'right', 'down_right'):
            self.hit_rect.left = self.player.hit_rect.right
        elif  self.player.direction in ('up_left', 'left', 'down_left'):
            self.hit_rect.right = self.player.hit_rect.left
        elif  self.player.direction == 'up':
            self.hit_rect.bottom = self.player.hit_rect.top
        elif  self.player.direction == 'down':
            self.hit_rect.top = self.player.hit_rect.bottom



        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= KNIGHT_SPECIAL_DMG
                # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
                if isinstance(skeleton, EliteOrc):
                    if skeleton.state != 'attack2':
                        skeleton.state = 'hurt'
                elif not isinstance(skeleton, Necromancer):
                    skeleton.state = 'hurt'
                self.damaged_enemies.add(skeleton)
        
        if now - self.last_update >= self.attack_duration:
            self.kill()

        self.rect.center = self.hit_rect.center





