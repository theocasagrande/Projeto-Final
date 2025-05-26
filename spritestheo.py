import pygame
import os
from config import *
from assets import load_assets
from game_screen import *
from spriteszaltron import *
import random
import math


vec = pygame.math.Vector2
# Função que confere se o hit_rect de um sprite colidiu com outro. Retorna um valor booleano
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)

# Função que confere se o hit_rect de um sprite esta colidindo com as paredes do mapa.
# Se colidir, o sprite não continua se movendo naquela direção e fica grudado na lateral da parede
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
#Função que acha a distancia entre 2 sprites
def distance_to(sprite1, sprite2):
    dx = sprite2.rect.centerx - sprite1.rect.centerx
    dy = sprite2.rect.centery - sprite1.rect.centery
    return (dx**2 + dy**2) ** 0.5
#Função que acha a distancia entre um sprite e um grupo de sprites
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
    #Função Construtora
    def __init__(self, x, y, state, player, game_walls, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.all_skeletons = player.all_skeletons
        self.animation_frames = self.assets['skeleton_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]

        self.walk_frames = self.assets['skeleton_walk']
        self.current_walk_frame = 0

        self.attack_frames = self.assets['skeleton_attack']
        self.current_attack_frame = 0

        self.hurt_frames = self.assets['skeleton_hurt']
        self.current_hurt_frame = 0

        self.death_frames = self.assets['skeleton_death']
        self.current_death_frame = 0

        self.collided = False
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = SKELETON_HEALTH
        self.total_health = SKELETON_HEALTH
        self.last_attack = 0


    # Função que evita que mobs se agrupem quando vão em direção ao player
    def avoid_mobs(self):
        for mob in self.all_skeletons:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()


            
    def update(self, dt):

        # Animações de morte do esqueleto
        if self.state == 'death':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            now = pygame.time.get_ticks()
            if now - self.last_update > 200:
                self.last_update = now
                if self.current_death_frame < len(self.death_frames):
                    self.image = self.death_frames[self.current_death_frame]
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_death_frame += 1
                else:
                    self.kill()
        # Ativa a animação de ataque se o esqueleto collidir com o hit_Rect do player
        
        if collide_hit_rect(self, self.player):
            now = pygame.time.get_ticks()
            if now - self.last_attack > 1000:  # 1 segundo
                self.state = 'attack'
                self.last_attack = now

        # Se o player estiver entre 5 tiles de distancia do esqueleto, 
        # o esqueleto começa a ir em direção ao player, evitando collidir com outros esqueletos
        if self.state != 'death' and self.state != 'attack':
            if distance_to(self.player, self) <= 5*TILESIZE:
                if self.state != 'hurt':
                    self.state = 'move'
                self.rot = (self.player.pos - self.pos).angle_to(vec(1, 0))
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                if self.acc != vec(0,0):
                    self.acc.scale_to_length(MOB_SPEED)
                self.acc += self.vel * -1
                self.vel += self.acc * dt
                self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
            else:
                self.state = 'idle'

        #Animação de ataque do esqueleto
        if self.state == 'attack':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack_frame < len(self.attack_frames):
                    self.image = self.attack_frames[self.current_attack_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack_frame += 1
                else:
                    self.current_attack_frame = 0
                    self.collided = False
                    self.state = 'idle'

        # Animação de tomar dano do esqueleto
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
        
        # Animação do esqueleto parado e em movimento. Essas animações só acontecem se o esqueleto não
        # estiver tomando dano, atacando ou morrendo
        if self.state not in ('attack', 'hurt', 'death'):
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
                    if self.current_frame >= len(self.animation_frames):
                        self.current_frame = 0
                    self.image = self.animation_frames[self.current_frame]
                    self.current_frame += 1
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
            elif self.state == 'move':
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
                    if self.current_walk_frame >= len(self.walk_frames):
                        self.current_walk_frame = 0
                    self.image = self.walk_frames[self.current_walk_frame]
                    self.current_walk_frame += 1
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
            self.state = 'death'

#Esqueleto Arqueiro
class SkeletonArcher(pygame.sprite.Sprite):
    #Função Construtora
    def __init__(self, x, y, state, player, game_walls, assets, enemy_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.all_sprites = player.all_sprites
        self.enemy_projectiles = enemy_projectiles
        self.all_projectiles = player.all_projectiles
        self.animation_frames = self.assets['skeleton_archer_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]


        self.attack_frames = self.assets['skeleton_archer_attack']
        self.current_attack_frame = 0

        self.collided = False
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = SKELETON_ARCHER_HEALTH
        self.total_health = SKELETON_ARCHER_HEALTH
        self.last_attack = 0

    #Cria uma flecha
    def shoot_arrow(self):
        arrow = SkeletonArcherArrow(self,self.player,self.assets, self.enemy_projectiles)
        self.all_sprites.add(arrow, layer=self.player._layer)
        self.all_projectiles.add(arrow)
    def update(self, dt):
    
        # Se a distancia entre o esqueleto arqueiro e o player for menor que 10 tiles, 
        # o esqueleto arqueiro atira uma flecha e ativa a animação de ataque dele.
        # A flecha é atirada uma vez a cada 3 segundos
        if self.state != 'death':
            if distance_to(self.player, self) <= 10*TILESIZE:
                self.state = 'attack'
                now = pygame.time.get_ticks()
                if now - self.last_attack > 3000:  # 3 segundos
                    self.shoot_arrow()
                    self.last_attack = now

        # Animação de ataque
        if self.state == 'attack':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack_frame < len(self.attack_frames):
                    self.image = self.attack_frames[self.current_attack_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack_frame += 1
                else:
                    self.current_attack_frame = 0
                    self.collided = False
                    self.state = 'idle'
        
        #Animação de tomar dano e do esqueleto parado
        if self.state not in ('attack', 'hurt'):
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
            self.kill()

#Flecha do Esqueleto Arqueiro
class SkeletonArcherArrow(pygame.sprite.Sprite):
    #Função Construtora
    def __init__(self, skeletonarcher, player, assets, enemy_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.original_image = self.assets['skeleton_archer_arrow'][0]
        self.skeleton_archer = skeletonarcher
        self.player = player
        self.enemy_projectiles = enemy_projectiles


        #Perguntar para ChatGPT como funciona
        archer_pos = self.skeleton_archer.rect.center
        player_pos = self.player.rect.center
        dx = player_pos[0] - archer_pos[0]
        dy = player_pos[1] - archer_pos[1]
        

        angle = math.degrees(math.atan2(-dy, dx)) 
        
       
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=archer_pos)
        
        if (dx, dy) != (0, 0):
            direction = pygame.math.Vector2(dx, dy).normalize()  
            self.velocity = direction * ARROW_SPEED
        else:
            self.velocity = pygame.math.Vector2(1, 0)
        
        self.hit_rect = SKELETON_ARCHER_ARROW_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.enemy_projectiles.add(self)

    def update(self, dt):
        
        #Atualiza posições dos rects
        self.rect.centerx += self.velocity.x * dt
        self.rect.centery += self.velocity.y * dt
        self.hit_rect.center = self.rect.center


        # Se collidir com o player, o player toma dano e a flecha desaparece.
        if collide_hit_rect(self, self.player):
            self.player.health -= SKELETON_ARCHER_ARROW_DAMAGE
            self.player.state = 'hurt'
            self.kill()
        #Se a flecha collidir com uma parede, ela desaparece.
        for wall in self.player.game_walls:
            if pygame.sprite.collide_rect(self, wall):
                self.kill()



class EliteOrc(pygame.sprite.Sprite):
    def __init__(self, x, y, state, player, game_walls, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.all_skeletons = player.all_skeletons
        self.animation_frames = self.assets['elite_orc_idle']
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.image = self.animation_frames[self.current_frame]

        self.walk_frames = self.assets['elite_orc_walk']
        self.current_walk_frame = 0

        self.attack_frames = self.assets['elite_orc_attack1']
        self.current_attack_frame = 0

        self.attack2_frames = self.assets['elite_orc_attack2']
        self.current_attack2_frame = 0

        self.hurt_frames = self.assets['elite_orc_hurt']
        self.current_hurt_frame = 0

        self.death_frames = self.assets['elite_orc_death']
        self.current_death_frame = 0

        self.rect = self.image.get_rect()
        self.hit_rect = ELITE_ORC_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.facing_right = True
        self.health = ELITE_ORC_HEALTH
        self.total_health = ELITE_ORC_HEALTH
        self.last_attack = pygame.time.get_ticks()
        self.last_attack2 = 0
        self.original_speed = ELITE_ORC_SPEED
        self.speed = ELITE_ORC_SPEED
        self.animationcount = 0


    # Função que evita que mobs se agrupem quando vão em direção ao player
    def avoid_mobs(self):
        for mob in self.all_skeletons:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()



            
    def update(self, dt):

        # Animações de morte do esqueleto
        if self.state == 'death':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            now = pygame.time.get_ticks()
            if now - self.last_update > 200:
                self.last_update = now
                if self.current_death_frame < len(self.death_frames):
                    self.image = self.death_frames[self.current_death_frame]
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_death_frame += 1
                else:
                    self.kill()
        # Ativa a animação de ataque se o esqueleto colidir com o hit_Rect do player
        if self.state != 'death':
            if collide_hit_rect(self, self.player):
                now = pygame.time.get_ticks()
                if now - self.last_attack > 1000:  # Só ataca após 1 segundo do último ataque
                    if self.state == 'attack2':
                        self.player.health -= ELITE_ORC_ATTACK2_DMG
                    else:
                        self.state = 'attack'
                        self.player.health -= ELITE_ORC_DMG
                    self.speed = self.original_speed
                    self.last_attack = now 

        # Se o player estiver entre 5 tiles de distancia do esqueleto, 
        # o esqueleto começa a ir em direção ao player, evitando collidir com outros esqueletos
        if self.state != 'death':
            if distance_to(self.player, self) <= 5*TILESIZE:
                now = pygame.time.get_ticks()
                if now - self.last_attack2 > 10000:
                    self.state = 'attack2'
                    self.last_attack2 = now
                if self.state not in ('attack', 'attack2', 'hurt'):
                    self.state = 'move'
                self.rot = (self.player.pos - self.pos).angle_to(vec(1, 0))
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                if self.state == 'attack2':
                    self.speed = self.original_speed * 4
                if self.acc != vec(0,0):
                    self.acc.scale_to_length(self.speed)
                self.acc += self.vel * -1
                self.vel += self.acc * dt
                self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
            else:
                self.state = 'idle'

        #Animação de ataque do esqueleto
        if self.state == 'attack':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            delta_x = self.player.pos.x - self.pos.x
            self.facing_right = delta_x >= 0

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if self.current_attack_frame < len(self.attack_frames):
                    self.image = self.attack_frames[self.current_attack_frame]
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_attack_frame += 1
                else:
                    self.current_attack_frame = 0
                    self.collided = False
                    self.state = 'idle'

        if self.state == 'attack2':
            self.vel = vec(1, 1)
            self.acc = vec(1, 1)
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
                    self.animationcount += 1
                    if self.animationcount >= 3:
                        self.animationcount = 0
                        self.state = 'idle'
                        self.speed = self.original_speed


        # Animação de tomar dano do esqueleto
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
        
        # Animação do esqueleto parado e em movimento. Essas animações só acontecem se o esqueleto não
        # estiver tomando dano, atacando ou morrendo
        if self.state not in ('attack','attack2', 'hurt', 'death'):
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
                    if self.current_frame >= len(self.animation_frames):
                        self.current_frame = 0
                    self.image = self.animation_frames[self.current_frame]
                    self.current_frame += 1
                    if not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
            elif self.state == 'move':
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
                    if self.current_walk_frame >= len(self.walk_frames):
                        self.current_walk_frame = 0
                    self.image = self.walk_frames[self.current_walk_frame]
                    self.current_walk_frame += 1
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
            self.state = 'death'


class Wizard(pygame.sprite.Sprite):
    #Função Construtora
    def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.game_walls = game_walls
        self.all_sprites = all_sprites
        self.assets = load_assets()
        self.all_skeletons = all_skeletons
        self.all_projectiles = all_projectiles

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.state = state
        self.frame_rate = 100

        self.original_frames = self.assets['wizard_idle']  
        self.animation_frames = list(self.original_frames)

        self.ice_attack_frames = self.assets['wizard_attack_ice_anim']
        self.original_ice_attack_frames = list(self.ice_attack_frames)

        self.hurt_frames = self.assets['wizard_hurt']
        self.original_hurt_frames = list(self.hurt_frames)

        self.special_frames = self.assets['wizard_special']
        self.original_special_frames = list(self.special_frames)

        self.speed_boost_frames = self.assets['wizard_speed_boost']
        self.original_speed_boost_frames= list(self.speed_boost_frames)

        self.current_frame = 0
        self.current_frameiceattack = 0
        self.current_hurt_frame = 0
        self.current_special_frame = 0
        self.current_speed_frame = 0

        self.hurt_duration = len(self.hurt_frames) * self.frame_rate
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos 
        self.iceticks = 1000
        self.specialticks = 5000
        self.speedticks = 10000
        self.speedticks = 10000
        self.last_ice_attack = pygame.time.get_ticks()
        self.last_special = pygame.time.get_ticks()
        self.direction = 'right'
        self.prev_direction = None
        self.last_update = pygame.time.get_ticks()
        self.original_walk_frames = self.assets['wizard_walk']
        self.walk_frames = list(self.original_walk_frames)
        self.current_framewalk = 0
        self.health = WIZARD_HEALTH
        self.total_health = WIZARD_HEALTH
        self.last_hit_time = 0
        self.last_speed = 0
        self.playerspeed = PLAYER_SPEED
        self.speedboost_cooldown = 8000
        self._layer = WIZARD_LAYER
        all_sprites.add(self, layer=self._layer)
        
      


    
    #Função que movimenta o player dependendo do botão pressionado, e ativa as habilidades
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        # Habilidades do Mago
        if self.state != 'hurt':
            if keys[pygame.K_SPACE]:
                if now - self.last_ice_attack > self.iceticks:
                    self.state = 'ice_attack'
                    self.ice_attack()
                    self.last_ice_attack = pygame.time.get_ticks()
            elif keys[pygame.K_f]:
                if now - self.last_special > self.specialticks:
                    self.state = 'special'
                    for i in range(5):
                        self.special_attack()
                    self.last_special = pygame.time.get_ticks()
            elif keys[pygame.K_c]:
                if now - self.last_speed > self.speedticks:
                    self.state = 'speed'
                    self.speedboost()
                
        #Movimentação Diagonal
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.vel = vec(-self.playerspeed, -self.playerspeed)
            self.direction = 'up_left'
            if self.state not in ('ice_attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.vel = vec(self.playerspeed, -self.playerspeed)
            self.direction = 'up_right'
            if self.state not in ('ice_attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.vel = vec(-self.playerspeed, self.playerspeed)
            self.direction = 'down_left'
            if self.state not in ('ice_attack', 'hurt', 'special'):
                self.state = 'walk'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.vel = vec(self.playerspeed, self.playerspeed)
            self.direction = 'down_right'
            if self.state not in ('ice_attack', 'hurt', 'special'):
                self.state = 'walk'

        #Movimentação horizontal e vertical
        else:
            if keys[pygame.K_LEFT]:
                self.vel.x = -self.playerspeed
                self.direction = 'left'
                if self.state not in ('ice_attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_RIGHT]:
                self.vel.x = self.playerspeed
                self.direction = 'right'
                if self.state not in ('ice_attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_UP]:
                self.vel.y = -self.playerspeed
                self.direction = 'up'
                if self.state not in ('ice_attack', 'hurt', 'special'):
                    self.state = 'walk'
            if keys[pygame.K_DOWN]:
                self.vel.y = self.playerspeed
                self.direction = 'down'
                if self.state not in ('ice_attack', 'hurt', 'special'):
                    self.state = 'walk'
        #Garante que a velocidade (self.vel) tenha sempre o mesmo tamanho, ou intensidade, independentemente da direção.
        # Isso foi feito para corrigir a velocidade em movimentos diagonais
        if self.vel.length() != 0:
            self.vel = self.vel.normalize() * self.playerspeed
        else:
            if self.state not in ('ice_attack', 'hurt', 'special'):
                self.state = 'idle'
            self.vel = vec(0, 0)



            
    def update(self, dt):
        self.get_keys()
        
        # Inverte a imagem se a direção do player mjdar
        if self.direction != self.prev_direction:
            self.rotate_image(self.direction)
            self.prev_direction = self.direction

        now = pygame.time.get_ticks()
        
        #Animação de ataque de gelo
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
        #Animação do mago quando ele ativa o ataque especial e a habilidade de aumentar velocidade do mago
        # essas duas habilidades têm a mesma animação
        if self.state in ('special', 'speed'):
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_special_frame += 1
                if self.current_special_frame >= len(self.special_frames):
                    self.state = 'idle'
                    self.current_special_frame = 0
                self.image = self.special_frames[self.current_special_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.centerx = self.pos.x
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center
        #Animação do player quando ele toma dano
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
        
        
        # Animação de movimentação do Mago. So ativa quando ele não estiver tomando dano, ou realizando um ataque
        if self.state not in ('ice_attack', 'hurt', 'special'):
          
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


        # Atualiza a posição dos rects e hit_rects 
        self.rect.center = self.pos
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        #verifica colisao com paredes
        collision(self, self.game_walls, 'x')
        self.hit_rect.centery = self.pos.y
        #verifica colisao com paredes
        collision(self, self.game_walls, 'y')
        self.rect.center = self.hit_rect.center

        # Quando a habilidade do speedboost termina, o mago volta a sua velocidade normal
        now2 = pygame.time.get_ticks()
        if now2 - self.last_speed >= self.speedboost_cooldown:
            self.playerspeed = PLAYER_SPEED

    #Função para criar o ataque de gelo
    def ice_attack(self):
            ice_attack = Wizard_attack_ice(self,self.pos, self.direction, self.all_skeletons, self.assets)
            self.all_sprites.add(ice_attack)
            self.all_projectiles.add(ice_attack)
    # Função para criar o ataque especial
    def special_attack(self):
        specialattack = WizardSpecial(self, self.rect.center, self.all_skeletons, self.assets)
        self.all_sprites.add(specialattack)
        self.all_projectiles.add(specialattack)
        self.last_special = pygame.time.get_ticks()
    # Função para ativar o speedboost
    def speedboost(self):
        speedboost1 = SpeedBoost(self)
        self.playerspeed *= 1.75
        self.all_sprites.add(speedboost1, layer=speedboost1._layer)
        self.last_speed = pygame.time.get_ticks()
        




        
    # Função que inverte as imagens se o player estiver indo para a esquerda. As imagens originais estão olhando para a direita, então
    #era preciso fazer isso.
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
        
        self.special_frames = [
            pygame.transform.flip(img, flip, False)
            for img in self.original_special_frames
        ]
        
 
        if self.state == 'walk':
            self.image = self.walk_frames[self.current_framewalk]
        elif self.state == 'ice_attack':
            self.image = self.ice_attack_frames[self.current_frameiceattack]
        elif self.state == 'hurt':
            self.image = self.hurt_frames[self.current_hurt_frame]
        elif self.state == 'special':
            self.image = self.special_frames[self.current_special_frame]
        else:
            self.image = self.animation_frames[self.current_frame]
      
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.hit_rect.center = self.rect.center


# Paredes do Jogo
class Obstacle(pygame.sprite.Sprite):
    #Função Construtora
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)  
        self.hit_rect = self.rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Suporta transparência
        self.image.fill((0, 0, 0, 0))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

#Camera do jogo que segue o player
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    #Aplica e posiciona camera no player
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    #Movimenta a camera de acordo com a posição do alvo levando em conta o tamanho da tela
    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
    #Posicionamento da camera para rects em vez de sprites
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    

# Ataque de gelo do mago    
class Wizard_attack_ice(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, player, center, direction, all_skeletons, assets):
        pygame.sprite.Sprite.__init__(self)
        self.all_skeletons = all_skeletons
        self.player = player
        self.animation_frames = assets['wizard_attack_ice']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = ICE_ATTACK_RECT.copy()
        self.damaged_enemies = set()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
    

        offset = 5 * TILESIZE
        cx, cy = center
        distance, target = distance_to_group(self.player, all_skeletons)
        # Posiciona o ataque de gelo em cima do inimigo se tiver perto o suficiente.
        if target and distance <= 5*TILESIZE:
            self.rect.center = target.rect.center
        # Se não estiver dentro de 5 tiles de distância, posiciona o ataque 5 tiles na direção que o mago está se movimentando (4 tiles na diagonal).
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


    # Animação do ataque
    def update(self):
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
                self.rect.center = old_center
                self.hit_rect.center = self.rect.center
        #Verifica colisão entre ataque de gelo e inimigos
        # Dentro do método update da classe Wizard_attack_ice:
        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= ICE_ATTACK_DMG
                # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
                if isinstance(skeleton, EliteOrc):
                    if skeleton.state != 'attack2':
                        skeleton.state = 'hurt'
                elif not isinstance(skeleton, Necromancer):
                    skeleton.state = 'hurt'
                self.damaged_enemies.add(skeleton)

# Ataque especial do mago
class WizardSpecial(pygame.sprite.Sprite):
    # Função Construtora
    def __init__(self, player, center, all_skeletons, assets):
        pygame.sprite.Sprite.__init__(self)
        self.all_skeletons = all_skeletons
        self.player = player
        self.animation_frames = assets['wizard_special_effect']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = WIZARD_SPECIAL_RECT.copy()
        self.damaged_enemies = set()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100


        self.rect.center = center
        self.rect.centerx = center[0]
        self.rect.centery = center[1]
        self.rect.centerx += random.randint(-2*TILESIZE,2*TILESIZE)
        self.rect.centery += random.randint(-2*TILESIZE, 2*TILESIZE)
        self.hit_rect.center = self.rect.center



    def update(self):
        #Animação do ataque
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
                self.hit_rect.center = self.rect.center
        #Verifica se colidiu com um inimigo
        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= WIZARD_SPECIAL_DMG
                # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
                if isinstance(skeleton, EliteOrc):
                    if skeleton.state != 'attack2':
                        skeleton.state = 'hurt'
                elif not isinstance(skeleton, Necromancer):
                    skeleton.state = 'hurt'
                self.damaged_enemies.add(skeleton)

#Habilidade de aumentar velocidade do mago
class SpeedBoost(pygame.sprite.Sprite):
    #Função Construtora
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.animation_frames = player.assets['wizard_speed_boost']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.time = pygame.time.get_ticks()
        self._layer = SPEEDBOOST_LAYER




    def update(self):
        #Posiciona o sprite debaixo do player
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery + self.player.rect.height // 2
        # Animação do speedboost
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1

            if now - self.time >= 8000:
                self.kill()
            if self.current_frame == len(self.animation_frames):
                self.current_frame = 0
            else:
                self.image = self.animation_frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.hit_rect.center = self.rect.center



class BossRoomTeleport(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)  
        self.hit_rect = self.rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Suporta transparência
        self.image.fill((0, 0, 0, 0))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Necromancer(pygame.sprite.Sprite):
    def __init__(self, x, y, state, player, game_walls, all_skeletons, assets, enemy_projectiles):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.player = player
        self.state = state
        self.game_walls = game_walls
        self.all_skeletons = all_skeletons
        self.all_sprites = player.all_sprites
        self.enemy_projectiles = enemy_projectiles
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

        self.attack_lockedon = False
        self.lockon_attempted = False
        self.lockon_attempted = False

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
        offset_x = random.randint(-2 * TILESIZE, 2 * TILESIZE)
        offset_y = random.randint(-2 * TILESIZE, 2 * TILESIZE)
        spawn_x = self.pos.x + offset_x
        spawn_y = self.pos.y + offset_y
        skeleton_archer1 = SkeletonArcher(spawn_x, spawn_y, 'idle', self.player, self.game_walls, self.assets, self.enemy_projectiles)
        self.all_skeletons.add(skeleton_archer1)
        self.all_sprites.add(skeleton_archer1)
    def attempt_lockon(self):
        self.lockon = AttackLockOn(self.player, self)
        self.lockon_saved_pos = self.player.hit_rect.center
        self.all_sprites.add(self.lockon)
    def attack3necro(self):
        for dir in ('up','down','left','right','up_right','up_left','down_left','down_right'):
            attack3 = NecromancerAttack3(self.player,self,dir)
            self.enemy_projectiles.add(attack3)
            self.all_sprites.add(attack3)
    def attempt_lockon(self):
        self.lockon = AttackLockOn(self.player, self)
        self.lockon_saved_pos = self.player.hit_rect.center
        self.all_sprites.add(self.lockon)
    def attack3necro(self):
        for dir in ('up','down','left','right','up_right','up_left','down_left','down_right'):
            attack3 = NecromancerAttack3(self.player,self,dir)
            self.enemy_projectiles.add(attack3)
            self.all_sprites.add(attack3)

    def update(self, dt):

        if self.state == 'death':
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            now = pygame.time.get_ticks()
            if now - self.last_update > 200:
                self.last_update = now
                if self.current_death_frame < len(self.death_frames):
                    self.image = self.death_frames[self.current_death_frame]
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.current_death_frame += 1
                else:
                    self.state = 'end_game'
    
        if self.state != 'death':
         
            if distance_to(self.player, self) <= 10*TILESIZE:
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
                if self.current_attack2_frame == 0 and not self.lockon_attempted:  
                    self.attempt_lockon()
                    self.lockon_attempted = True
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
                        self.lockon_attempted = False
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
                        self.attack3necro()
                        attack3player = NecromancerAttack3(self.player, self, 'player')
                        self.enemy_projectiles.add(attack3player)
                        self.all_sprites.add(attack3player)

            
            #Animação de tomar dano e parado
            if self.state not in ('attack1','attack2', 'attack3'):
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

    def attack_loop(self):
        if self.state in ('death'):
            return 
        now = pygame.time.get_ticks()
        elapsed1 = now - self.last_attack_chain
        elapsed1 = now - self.last_attack_chain

      
        if elapsed1 > 5000 and not self.attack1_activated:
            self.state = 'attack1'
            self.attack1_activated = True

      
        if elapsed1 > 15000 and not self.attack2_activated:
            self.state = 'attack2'
            self.attack2_activated = True

    
        if elapsed1 > 25000 and not self.attack3_activated:
            self.state = 'attack3'
            self.attack3necro()
            self.attack3necro()
            self.attack3_activated = True

        # Reset após os 15 segundos
        if  self.attack1_activated and  self.attack2_activated and  self.attack3_activated:
            self.attack1_activated = False
            self.attack2_activated = False
            self.attack3_activated = False
            self.last_attack_chain = now
class AttackLockOn(pygame.sprite.Sprite):
    def __init__(self, player, necromancer):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.assets = player.assets
        self.all_sprites = player.all_sprites
        self.necromancer = necromancer
        self.player = player
        self.player = player
        self.image = self.assets['attack_lockon'][0]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.last_update = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.all_sprites.add(self)


    def update(self):
        now = pygame.time.get_ticks()
        elapsed2 = now - self.last_update
        if elapsed2 < 2000:
            elapsed2 = now - self.last_update
        if elapsed2 < 2000:
            self.hit_rect.center = self.player.hit_rect.center
            self.rect.center = self.hit_rect.center
            self.center_save = self.hit_rect.center
        elif elapsed2 < 3000:
            self.hit_rect.center = self.center_save
            self.rect.center = self.hit_rect.center
            self.rect.center = self.hit_rect.center
            self.center_save = self.hit_rect.center
        elif elapsed2 < 3000:
            self.hit_rect.center = self.center_save
            self.rect.center = self.hit_rect.center
        else:
            if collide_hit_rect(self, self.player) and not self.necromancer.attack_lockedon:
                self.necromancer.attack_lockedon = True
                attack2 = NecromancerAttack2(self.player, self, self.necromancer)
                self.all_sprites.add(attack2)
                attack2 = NecromancerAttack2(self.player, self, self.necromancer)
                self.all_sprites.add(attack2)
            self.kill()
           
        
           
        

class NecromancerAttack2(pygame.sprite.Sprite):
    def __init__(self, player, lockonsprite, necromancer):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.lockonsprite = lockonsprite
        self.necromancer = necromancer
        self.animation_frames = self.player.assets['necromancer_attack2_effect']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = NECRO_ATTACK2_HITRECT.copy()
        self.hit_rect.center = self.lockonsprite.center_save
        self.rect.center = self.hit_rect.center
        self.last_update = 0
        self.current_animation_frame = 0
        self.frame_rate = 100
        self.hit_rect.center = lockonsprite.center_save  
        self.rect.center = self.hit_rect.center
        self.player_hit = False

    def update(self):

        if collide_hit_rect(self, self.player) and not self.player_hit:
            self.player.health -= NECRO_ATTACK2_DMG
            self.player.state = 'hurt'
            self.player_hit = True
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.current_animation_frame < len(self.animation_frames):
                self.image = self.animation_frames[self.current_animation_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.current_animation_frame += 1
            else:
                self.necromancer.attack_lockedon = False
                self.kill()

class NecromancerAttack3(pygame.sprite.Sprite):
        def __init__(self, player, necromancer, direction):
            pygame.sprite.Sprite.__init__(self)
            self.player = player
            self.necromancer = necromancer
            self.image = self.player.assets['necromancer_attack3_effect'][0]
            self.original_image = self.player.assets['necromancer_attack3_effect'][0]
            self.rect = self.image.get_rect()
            self.hit_rect = NECRO_ATTACK3_HIT_RECT.copy()
            self.hit_rect.center = self.necromancer.hit_rect.center
            self.direction = direction
            self.enemy_projectiles = self.necromancer.enemy_projectiles
            self.pos = vec(self.necromancer.rect.center)  # Start at necromancer's center
            self.vel = vec(0, 0)

            self.enemy_projectiles.add(self)


            if direction == 'player':
                target_pos = vec(self.player.rect.center)
                direction_vector = target_pos - self.pos
                if direction_vector.length() > 0:
                    self.vel = direction_vector.normalize() * NECRO_ATTACK3_SPEED
                else:
                    self.vel = vec(0, 0) 
                angle = math.degrees(math.atan2(-direction_vector.y, direction_vector.x))
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.pos)
            else:
                speed = NECRO_ATTACK3_SPEED
                if direction == 'up':
                    self.pos.y = self.necromancer.rect.top - self.hit_rect.height / 2
                    self.vel = vec(0, -speed)
                    angle = 90
                elif direction == 'down':
                    self.pos.y = self.necromancer.rect.bottom + self.hit_rect.height / 2
                    self.vel = vec(0, speed)
                    angle = -90
                elif direction == 'left':
                    self.pos.x = self.necromancer.rect.left - self.hit_rect.width / 2
                    self.vel = vec(-speed, 0)
                    angle = 180
                elif direction == 'right':
                    self.pos.x = self.necromancer.rect.right + self.hit_rect.width / 2
                    self.vel = vec(speed, 0)
                    angle = 0
                elif direction == 'up_right':
                    self.pos = vec(self.necromancer.rect.right + self.hit_rect.width / 2,
                                self.necromancer.rect.top - self.hit_rect.height / 2)
                    self.vel = vec(speed, -speed).normalize() * speed
                    angle = 45
                elif direction == 'up_left':
                    self.pos = vec(self.necromancer.rect.left - self.hit_rect.width / 2,
                                self.necromancer.rect.top - self.hit_rect.height / 2)
                    self.vel = vec(-speed, -speed).normalize() * speed
                    angle = 135
                elif direction == 'down_right':
                    self.pos = vec(self.necromancer.rect.right + self.hit_rect.width / 2,
                                self.necromancer.rect.bottom + self.hit_rect.height / 2)
                    self.vel = vec(speed, speed).normalize() * speed
                    angle = -45
                elif direction == 'down_left':
                    self.pos = vec(self.necromancer.rect.left - self.hit_rect.width / 2,
                                self.necromancer.rect.bottom + self.hit_rect.height / 2)
                    self.vel = vec(-speed, speed).normalize() * speed
                    angle = 225
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.pos)

            self.hit_rect.center = self.pos
            
        def update(self, dt):
            self.pos += self.vel * dt
            self.rect.center = self.pos
            self.hit_rect.center = self.pos

            # Collision with player
            if collide_hit_rect(self, self.player):
                self.player.health -= NECRO_ATTACK3_DMG
                self.player.state = 'hurt'
                self.kill()
            # Collision with walls
            for wall in self.player.game_walls:
                if pygame.sprite.collide_rect(self, wall):
                    self.kill()




        





            







class NecromancerAttack2(pygame.sprite.Sprite):
    def __init__(self, player, lockonsprite, necromancer):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.lockonsprite = lockonsprite
        self.necromancer = necromancer
        self.animation_frames = self.player.assets['necromancer_attack2_effect']
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = NECRO_ATTACK2_HITRECT.copy()
        self.hit_rect.center = self.lockonsprite.center_save
        self.rect.center = self.hit_rect.center
        self.last_update = 0
        self.current_animation_frame = 0
        self.frame_rate = 100
        self.hit_rect.center = lockonsprite.center_save  
        self.rect.center = self.hit_rect.center
        self.player_hit = False

    def update(self):

        if collide_hit_rect(self, self.player) and not self.player_hit:
            self.player.health -= NECRO_ATTACK2_DMG
            self.player.state = 'hurt'
            self.player_hit = True
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.current_animation_frame < len(self.animation_frames):
                self.image = self.animation_frames[self.current_animation_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.current_animation_frame += 1
            else:
                self.necromancer.attack_lockedon = False
                self.kill()

class NecromancerAttack3(pygame.sprite.Sprite):
        def __init__(self, player, necromancer, direction):
            pygame.sprite.Sprite.__init__(self)
            self.player = player
            self.necromancer = necromancer
            self.image = self.player.assets['necromancer_attack3_effect'][0]
            self.original_image = self.player.assets['necromancer_attack3_effect'][0]
            self.rect = self.image.get_rect()
            self.hit_rect = NECRO_ATTACK3_HIT_RECT.copy()
            self.hit_rect.center = self.necromancer.hit_rect.center
            self.direction = direction
            self.enemy_projectiles = self.necromancer.enemy_projectiles
            self.pos = vec(self.necromancer.rect.center)  # Start at necromancer's center
            self.vel = vec(0, 0)

            self.enemy_projectiles.add(self)


            if direction == 'player':
                target_pos = vec(self.player.rect.center)
                direction_vector = target_pos - self.pos
                if direction_vector.length() > 0:
                    self.vel = direction_vector.normalize() * NECRO_ATTACK3_SPEED
                else:
                    self.vel = vec(0, 0) 
                angle = math.degrees(math.atan2(-direction_vector.y, direction_vector.x))
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.pos)
            else:
                speed = NECRO_ATTACK3_SPEED
                if direction == 'up':
                    self.pos.y = self.necromancer.rect.top - self.hit_rect.height / 2
                    self.vel = vec(0, -speed)
                    angle = 90
                elif direction == 'down':
                    self.pos.y = self.necromancer.rect.bottom + self.hit_rect.height / 2
                    self.vel = vec(0, speed)
                    angle = -90
                elif direction == 'left':
                    self.pos.x = self.necromancer.rect.left - self.hit_rect.width / 2
                    self.vel = vec(-speed, 0)
                    angle = 180
                elif direction == 'right':
                    self.pos.x = self.necromancer.rect.right + self.hit_rect.width / 2
                    self.vel = vec(speed, 0)
                    angle = 0
                elif direction == 'up_right':
                    self.pos = vec(self.necromancer.rect.right + self.hit_rect.width / 2,
                                self.necromancer.rect.top - self.hit_rect.height / 2)
                    self.vel = vec(speed, -speed).normalize() * speed
                    angle = 45
                elif direction == 'up_left':
                    self.pos = vec(self.necromancer.rect.left - self.hit_rect.width / 2,
                                self.necromancer.rect.top - self.hit_rect.height / 2)
                    self.vel = vec(-speed, -speed).normalize() * speed
                    angle = 135
                elif direction == 'down_right':
                    self.pos = vec(self.necromancer.rect.right + self.hit_rect.width / 2,
                                self.necromancer.rect.bottom + self.hit_rect.height / 2)
                    self.vel = vec(speed, speed).normalize() * speed
                    angle = -45
                elif direction == 'down_left':
                    self.pos = vec(self.necromancer.rect.left - self.hit_rect.width / 2,
                                self.necromancer.rect.bottom + self.hit_rect.height / 2)
                    self.vel = vec(-speed, speed).normalize() * speed
                    angle = 225
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.pos)

            self.hit_rect.center = self.pos
            
        def update(self, dt):
            self.pos += self.vel * dt
            self.rect.center = self.pos
            self.hit_rect.center = self.pos

            # Collision with player
            if collide_hit_rect(self, self.player):
                self.player.health -= NECRO_ATTACK3_DMG
                self.player.state = 'hurt'
                self.kill()
            # Collision with walls
            for wall in self.player.game_walls:
                if pygame.sprite.collide_rect(self, wall):
                    self.kill()
class Archer(pygame.sprite.Sprite):
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

        self.idle_frames = self.assets['archer_idle']  
        self.walk_frames = self.assets['archer_walk']
        self.attack_frames = self.assets['archer_attack']
        self.special_frames = self.assets['archer_special']
        self.hurt_frames = self.assets['archer_hurt']

        self.special_frames = self.assets['archer_special']



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
        arrow = Arrow(self.rect.centerx, self.rect.centery, self, self.direction)
        self.all_projectiles.add(arrow)
        self.all_sprites.add(arrow)
    # def special(self):
    #     special = KnightSpecialHitbox(self)
    #     self.all_sprites.add(special)
        

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

        

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, player, direction):
         pygame.sprite.Sprite.__init__(self)
         self.player = player
         self.original_image = player.assets['archer_flecha'][0]
         self.image = self.rotate_image(direction)
         self.all_skeletons = player.all_skeletons
         self.rect = self.image.get_rect()
         self.hit_rect = ARROW_HIT_RECT.copy()
         self.rect.center = (x, y)
         self.hit_rect.center = self.rect.center
         self.speed = 500
         self.direction = direction
         self.vx, self.vy = self.get_velocity_vector(direction)
         self.damaged_enemies = set()
    def rotate_image(self, direction):
         if direction == 'up':
             return pygame.transform.rotate(self.original_image, 90)
         elif direction == 'down':
             return pygame.transform.rotate(self.original_image, -90)
         elif direction == 'left':
             return pygame.transform.rotate(self.original_image, 180)
         elif direction == 'right':
             return pygame.transform.rotate(self.original_image, 0)
         elif direction == 'up_left':
             return pygame.transform.rotate(self.original_image, 135)
         elif direction == 'up_right':
             return pygame.transform.rotate(self.original_image, 45)
         elif direction == 'down_left':
             return pygame.transform.rotate(self.original_image, -135)
         elif direction == 'down_right':
             return pygame.transform.rotate(self.original_image, -45)
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
             return (0.707, 0.707)
    def update(self, dt):
        self.rect.x += self.vx * self.speed * dt
        self.rect.y += self.vy * self.speed * dt

        self.hit_rect.center = self.rect.center

        # Check for collision with walls
        hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
        for skeleton in hits:
            if skeleton not in self.damaged_enemies:
                skeleton.health -= ARCHER_ARROW_DMG
                # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
                if isinstance(skeleton, EliteOrc):
                    if skeleton.state != 'attack2':
                        skeleton.state = 'hurt'
                elif not isinstance(skeleton, Necromancer):
                    skeleton.state = 'hurt'
                self.damaged_enemies.add(skeleton)
        #Se a flecha collidir com uma parede, ela desaparece.
        for wall in self.player.game_walls:
            if pygame.sprite.collide_rect(self, wall):
                self.kill()

         

    

                






        





            













