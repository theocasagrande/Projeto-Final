import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spriteszaltron import *


vec = pygame.math.Vector2
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
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
    

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, state, player, game_walls):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.animation_frames = self.assets['skeleton_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = SKELETON_HEALTH

    def update(self, dt):
        if distance_to(self.player, self) <= 5*TILESIZE:
            self.rot = (self.player.pos - self.pos).angle_to(vec(1, 0))
            self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * dt
            self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
    
        if self.state == 'idle':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            if delta_x < 0:
                self.facing_right = False
            else: 
                self.facing_right = True
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.animation_frames):
                    self.current_frame = 0
                self.image = self.animation_frames[self.current_frame]
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    def draw_health(self):
        if self.health >= 60:
            col = (0, 255, 0)
        elif self.health >= 30:
            col = YELLOW
        else:
            col = (255, 0, 0)
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pygame.Rect(0,0, width, 7)
        if self.health < 100:
            pygame.draw.rect(self.image, col, self.health_bar)
        
class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.game_walls = game_walls
        self.all_sprites = all_sprites
        self.assets = load_assets()
        self.all_skeletons = all_skeletons
        self.all_projectiles = all_projectiles

        self.vel = vec(0, 0)
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.state = state
        self.frame_rate = 100
        self.original_frames = self.assets['wizard_idle']  
        self.animation_frames = list(self.original_frames)
        self.ice_attack_frames = self.assets['wizard_attack_ice_anim']
        self.original_ice_attack_frames = list(self.ice_attack_frames)
        self.hurt_frames = self.assets['wizard_hurt']
        self.original_hurt_frames = list(self.hurt_frames)
        self.current_frame = 0
        self.current_frameiceattack = 0
        self.current_hurt_frame = 0
        self.hurt_duration = len(self.hurt_frames) * self.frame_rate
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos 
        self.iceticks = 1000
        self.last_ice_attack = pygame.time.get_ticks()
        self.direction = 'right'
        self.prev_direction = None
        self.last_update = pygame.time.get_ticks()
        self.original_walk_frames = self.assets['wizard_walk']
        self.walk_frames = list(self.original_walk_frames)
        self.current_framewalk = 0
        self.health = PLAYER_HEALTH
      


    

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()

        if self.state != 'hurt':
            if keys[pygame.K_SPACE]:
                self.state = 'ice_attack'
                self.ice_attack()
        # Handle diagonals first
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, -1)
            self.direction = 'up_left'
            if self.state not in ('ice_attack', 'hurt'):
                self.state = 'walk'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, -1)
            self.direction = 'up_right'
            if self.state not in ('ice_attack', 'hurt'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.vel = vec(-1, 1)
            self.direction = 'down_left'
            if self.state not in ('ice_attack', 'hurt'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.vel = vec(1, 1)
            self.direction = 'down_right'
            if self.state not in ('ice_attack', 'hurt'):
                self.state = 'walk'
        else:
            if keys[pygame.K_LEFT]:
                self.vel.x = -1
                self.direction = 'left'
                if self.state not in ('ice_attack', 'hurt'):
                    self.state = 'walk'
            if keys[pygame.K_RIGHT]:
                self.vel.x = 1
                self.direction = 'right'
                if self.state not in ('ice_attack', 'hurt'):
                    self.state = 'walk'
            if keys[pygame.K_UP]:
                self.vel.y = -1
                self.direction = 'up'
                if self.state not in ('ice_attack', 'hurt'):
                    self.state = 'walk'
            if keys[pygame.K_DOWN]:
                self.vel.y = 1
                self.direction = 'down'
                if self.state not in ('ice_attack', 'hurt'):
                    self.state = 'walk'
                
        if self.vel.length() != 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
        else:
            if self.state not in ('ice_attack', 'hurt'):
                self.state = 'idle'
            self.vel = vec(0, 0)



            
    def update(self, dt):
        self.get_keys()
        
        if self.direction != self.prev_direction:
            self.rotate_image(self.direction)
            self.prev_direction = self.direction

        now = pygame.time.get_ticks()
        
  
        if self.state == 'ice_attack':
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frameiceattack += 1
                if self.current_frameiceattack >= len(self.ice_attack_frames):
                    self.state = 'idle'
                    self.current_frameiceattack = 0
                self.image = self.ice_attack_frames[self.current_frameiceattack]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center

        if self.state == 'hurt':
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

        else:
          
            if self.state == 'walk':
                frames = self.walk_frames
                current_frame = self.current_framewalk
            else: 
                frames = self.animation_frames
                current_frame = self.current_frame

   
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                current_frame = (current_frame + 1) % len(frames)
                self.image = frames[current_frame]
                
    
                if self.state == 'walk':
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


    def ice_attack(self):
        
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_ice_attack
        if elapsed_ticks > self.iceticks:
            self.last_ice_attack = now
            self.current_frameiceattack = 0
            self.last_update = pygame.time.get_ticks()
            self.image = self.ice_attack_frames[0]
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            ice_attack = Wizard_attack_ice(self,self.pos, self.direction, self.all_skeletons, self.assets)
            self.all_sprites.add(ice_attack)
            self.all_projectiles.add(ice_attack)
        

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
            for img in self.original_ice_attack_frames
        ]

        self.hurt_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_hurt_frames
        ]
        
 
        if self.state == 'walk':
            self.image = self.walk_frames[self.current_framewalk]
        elif self.state == 'ice_attack':
            self.image = self.ice_attack_frames[self.current_frameiceattack]
        elif self.state == 'hurt':
            self.image = self.hurt_frames[self.current_hurt_frame]
        else:
            self.image = self.animation_frames[self.current_frame]
      
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.hit_rect.center = self.rect.center

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.assets = load_assets()
        self.image = self.assets['wall_tile']
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
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
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
class Wizard_attack_ice(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player, center, direction, all_skeletons, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.all_skeletons = all_skeletons
        self.player = player
        self.animation_frames = self.assets['wizard_attack_ice']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.damaged_enemies = set()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
    
       
        offset = 5 * TILESIZE
        cx, cy = center
        distance, target = distance_to_group(self.player, all_skeletons)

        if target and distance <= 5*TILESIZE:
            self.rect.center = target.rect.center
        else:
            # Calculate direction-based offset
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



    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.animation_frames):
                self.kill()
                self.collided = False
            else:
                self.image = self.animation_frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
        hits = pygame.sprite.spritecollide(
        self, 
        self.all_skeletons, 
        False, 
        pygame.sprite.collide_rect
        )
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= ICE_ATTACK_DMG
                self.damaged_enemies.add(skeleton)