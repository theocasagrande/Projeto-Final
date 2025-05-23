import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spriteszaltron import *
import random
import math


class Necromancer(pygame.sprite.Sprite):
    def __init__(self, x, y, state, player, game_walls, all_skeletons, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.all_skeletons = all_skeletons
        self.all_sprites = player.all_sprites
        self.animation_frames = self.assets['necromancer_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]

        self.walk_frames = self.assets['necromancer_walk']
        self.current_walk_frame = 0

        self.attack1_frames = self.assets['necromancer_attack1']
        self.current_attack1_frame = 0

        self.attack2_frames = self.assets['necromancer_attack2']
        self.current_attack2_frame = 0

        self.attack3_frames = self.assets['necromancer_attack3']
        self.current_attack3_frame = 0

        self.death_frames = self.assets['necromancer_death']
        self.current_death_frame = 0

        self.hurt_frames = self.assets['necromancer_hurt']
        self.current_hurt_frame = 0

        self.collided = False
        self.rect = self.image.get_rect()
        self.hit_rect = BOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = BOSS_HEALTH
        self.total_health = BOSS_HEALTH
        self.last_attack_chain = 0
        self.attack1_activated = False
        self.attack2_activated = False
        self.attack3_activated = False

    def avoid_mobs(self):
        for mob in self.all_skeletons:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def attack1necro(self):
        for i in range(3):
            offset_x = random.randint(-2 * TILESIZE, 2 * TILESIZE)
            offset_y = random.randint(-2 * TILESIZE, 2 * TILESIZE)
            spawn_x = self.pos.x + offset_x
            spawn_y = self.pos.y + offset_y
            skeleton1 = Skeleton(spawn_x, spawn_y, 'idle', self.player, self.game_walls, self.assets)
            self.all_skeletons.add(skeleton1)
            self.all_sprites.add(skeleton1)


    def update(self, dt):
    
        
        if distance_to(self.player, self) <= 15*TILESIZE:
            self.attack_loop()
            if self.state not in ('attack1', 'attack2', 'attack3', 'hurt'):
                self.state = 'move'
            self.rot = (self.player.pos - self.pos).angle_to(vec(1, 0))
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(BOSS_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * dt
            self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2

        # Animação de ataque
        if self.state == 'attack1':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack1_frame < len(self.attack1_frames):
                    self.image = self.attack1_frames[self.current_attack1_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack1_frame += 1
                else:
                    self.current_attack1_frame = 0
                    self.state = 'idle'
                    self.attack1necro()
        if self.state == 'attack2':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack2_frame < len(self.attack2_frames):
                    self.image = self.attack2_frames[self.current_attack2_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack2_frame += 1
                else:
                    self.current_attack2_frame = 0
                    self.state = 'idle'
        if self.state == 'attack3':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack3_frame < len(self.attack3_frames):
                    self.image = self.attack3_frames[self.current_attack3_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack3_frame += 1
                else:
                    self.current_attack3_frame = 0
                    self.state = 'idle'
        if self.state == 'hurt':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            now = pygame.time.get_ticks()
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_hurt_frame >= len(self.hurt_frames):
                    self.state = 'idle'
                    self.current_hurt_frame = 0
                self.image = self.hurt_frames[self.current_hurt_frame]
                self.current_hurt_frame += 1
                if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center
        
        #Animação de tomar dano e parado
        if self.state not in ('attack1', 'hurt', 'attack2', 'attack3'):
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
            if self.state == 'move':
                self.vel = vec(0, 0)
                self.acc = vec(0, 0)
                delta_x = self.player.pos.x - self.pos.x
                self.facing_right = delta_x >= 0

                now = pygame.time.get_ticks()
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    if self.current_walk_frame < len(self.walk_frames):
                        self.image = self.walk_frames[self.current_walk_frame]
                        if not self.facing_right:
                            self.image = pygame.transform.flip(self.image, True, False)
                        old_center = self.rect.center
                        self.rect = self.image.get_rect()
                        self.rect.center = old_center
                        self.current_walk_frame += 1
                    else:
                        self.current_walk_frame = 0
                        self.state = 'idle'
            

        #Atualiza posição dos rects
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x

        #Verifica colisões entre paredes
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center

        # Remove o esqueleto arqueiro de todos os grupos se ele morrer (vida acabar)
        if self.health <= 0:
            self.state = 'death'
            self.kill()

    def attack_loop(self):
        if self.state in ('attack1', 'attack2', 'attack3', 'hurt', 'death'):
            return 
        now = pygame.time.get_ticks()
        elapsed = now - self.last_attack_chain

        # Ataque 1 ocorre primeiro
        if elapsed <= 5000 and not self.attack1_activated:
            self.state = 'attack1'
            self.attack1_activated = True

        # Ataque 2 ocorre depois de 5 segundos
        elif elapsed <= 10000 and not self.attack2_activated:
            self.state = 'attack2'
            self.attack2_activated = True

        # Ataque 3 ocorre depois de 10 segundos
        elif elapsed <= 15000 and not self.attack3_activated:
            self.state = 'attack3'
            self.attack3_activated = True

        # Reset após os 15 segundos
        elif elapsed > 15000:
            self.attack1_activated = False
            self.attack2_activated = False
            self.attack3_activated = False
            self.last_attack_chain = now

