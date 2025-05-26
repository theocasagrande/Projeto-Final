# import pygame
# import os
# from config import *
# from assets import load_assets
# from game_screen import *
# from spritestheo import *
# vec = pygame.math.Vector2


# def collide_hit_rect(one, two):
#     return one.hit_rect.colliderect(two.hit_rect)
# def collision(sprite, group, dir):
#     if dir == 'x':
#         hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#         if hits:
#             if hits[0].rect.centerx > sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
#             if hits[0].rect.centerx < sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
#             sprite.vel.x = 0
#             sprite.hit_rect.centerx = sprite.pos.x
#             sprite.pos.x = sprite.hit_rect.centerx

#     if dir == 'y':
#         hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#         if hits:
#             if hits[0].rect.centery > sprite.hit_rect.centery:
#                 sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
#             if hits[0].rect.centery < sprite.hit_rect.centery:
#                 sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
#             sprite.vel.y = 0
#             sprite.hit_rect.centery = sprite.pos.y
#             sprite.pos.y = sprite.hit_rect.centery
# def distance_to(sprite1, sprite2):
#     dx = sprite2.rect.centerx - sprite1.rect.centerx
#     dy = sprite2.rect.centery - sprite1.rect.centery
#     return (dx**2 + dy**2) ** 0.5
# #Função que acha a distancia entre um sprite e um grupo de sprites
# def distance_to_group(sprite, group):
#     smallestdistance = 10000
#     if len(group) != 0:
#         for enemy in group:
#             distance = distance_to(sprite, enemy)
#             if distance <= smallestdistance:
#                 smallestdistance = distance
#                 target = enemy
#         return smallestdistance, target
#     else:
#         return smallestdistance, None
# class Archer(pygame.sprite.Sprite):
#     def __init__(self, x, y, state, all_sprites, game_walls, all_skeletons, all_projectiles):
#         pygame.sprite.Sprite.__init__(self)
#         self.assets = load_assets()
#         self.game_walls = game_walls
#         self.all_sprites = all_sprites
#         self.all_skeletons = all_skeletons
#         self.all_projectiles = all_projectiles

#         self.vel = vec(0, 0)
#         self.pos = vec(x, y)
#         self.state = state
#         self.frame_rate = 100
#         self.special_frame_rate = 150
#         self.direction = 'right'
#         self.prev_direction = None
#         self.last_update = pygame.time.get_ticks()

#         self.idle_frames = self.assets['archer_idle']  
#         self.walk_frames = self.assets['archer_walk']
#         self.attack_frames = self.assets['archer_attack']
#         self.special_frames = self.assets['archer_special']
#         self.hurt_frames = self.assets['archer_hurt']

#         self.special_frames = self.assets['archer_special']



#         self.original_idle = list(self.idle_frames)
#         self.original_walk = list(self.walk_frames)
#         self.original_attack = list(self.attack_frames)
#         self.original_special = list(self.special_frames)
#         self.original_hurt = list(self.hurt_frames)

#         self.current_frame = 0
#         self.current_attack_frame = 0
#         self.current_special_frame = 0
#         self.current_walk_frame = 0
#         self.current_hurt_frame = 0

#         self.image = self.idle_frames[self.current_frame]
#         self.rect = self.image.get_rect()
#         self.original_hit_rect_width = PLAYER_HIT_RECT.width
#         self.original_hit_rect_height = PLAYER_HIT_RECT.height
#         self.hit_rect = PLAYER_HIT_RECT.copy()
#         self.hit_rect.center = self.rect.center
#         self.original_hit_rect_center = self.hit_rect.center
#         self.rect.center = self.pos

#         self.health = KNIGHT_HEALTH
#         self.total_health = KNIGHT_HEALTH
#         self.attack_cooldown = 800
#         self.special_cooldown = 5000
#         self.last_attack = 0
#         self.last_special = 0
#         self.last_hit_time = 0
#         self.playerspeed = PLAYER_SPEED
#         self.damaged_enemies = set()
#         self._layer = WIZARD_LAYER
#         self.attack_offset = 0
#         all_sprites.add(self, layer=self._layer)


    
#     def get_keys(self):
#         self.vel = vec(0, 0)
#         keys = pygame.key.get_pressed()
#         now = pygame.time.get_ticks()

#         if self.state != 'hurt':
#             if keys[pygame.K_SPACE] and now - self.last_attack > self.attack_cooldown:
#                 self.state = 'attack'
#                 self.last_attack = now
#                 self.current_attack_frame = 0
#                 self.attack()
#             elif keys[pygame.K_f] and now - self.last_special > self.special_cooldown:
#                 self.state = 'special'
#                 self.last_special = now
#                 self.current_special_frame = 0
                

#         if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
#             self.vel = vec(-self.playerspeed, -self.playerspeed)
#             self.direction = 'up_left'
#             if self.state not in ('attack', 'hurt', 'special'):
#                 self.state = 'walk'
#         elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
#             self.vel = vec(self.playerspeed, -self.playerspeed)
#             self.direction = 'up_right'
#             if self.state not in ('attack', 'hurt', 'special'):
#                 self.state = 'walk'
#         elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
#             self.vel = vec(-self.playerspeed, self.playerspeed)
#             self.direction = 'down_left'
#             if self.state not in ('attack', 'hurt', 'special'):
#                 self.state = 'walk'
#         elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
#             self.vel = vec(self.playerspeed, self.playerspeed)
#             self.direction = 'down_right'
#             if self.state not in ('attack', 'hurt', 'special'):
#                 self.state = 'walk'
#         else:
#             if keys[pygame.K_LEFT]:
#                 self.vel.x = -self.playerspeed
#                 self.direction = 'left'
#                 if self.state not in ('attack', 'hurt', 'special'):
#                     self.state = 'walk'
#             if keys[pygame.K_RIGHT]:
#                 self.vel.x = self.playerspeed
#                 self.direction = 'right'
#                 if self.state not in ('attack', 'hurt', 'special'):
#                     self.state = 'walk'
#             if keys[pygame.K_UP]:
#                 self.vel.y = -self.playerspeed
#                 self.direction = 'up'
#                 if self.state not in ('attack', 'hurt', 'special'):
#                     self.state = 'walk'
#             if keys[pygame.K_DOWN]:
#                 self.vel.y = self.playerspeed
#                 self.direction = 'down'
#                 if self.state not in ('attack', 'hurt', 'special'):
#                     self.state = 'walk'

#         if self.vel.length() > 0:
#             self.vel = self.vel.normalize() * PLAYER_SPEED
#             if self.state not in ('attack', 'special', 'hurt'):
#                 self.state = 'walk'
#         else:
#             if self.state not in ('attack', 'special', 'hurt'):
#                 self.state = 'idle'
#     def attack(self):
#         arrow = Arrow(self.rect.centerx, self.rect.centery, self, self.direction)
#         self.all_projectiles.add(arrow)
#         self.all_sprites.add(arrow)
#     # def special(self):
#     #     special = KnightSpecialHitbox(self)
#     #     self.all_sprites.add(special)
        

#     def update(self, dt):
#         self.get_keys()
#         now = pygame.time.get_ticks()

#         if self.direction != self.prev_direction:
#             self.rotate_image(self.direction)
#             self.prev_direction = self.direction

#         if self.state == 'attack':
#             if now - self.last_update > self.frame_rate:
#                 self.last_update = now
#                 self.current_attack_frame += 1
#                 if self.current_attack_frame >= len(self.attack_frames):
#                     self.state = 'idle'
#                     self.current_attack_frame = 0
#                 self.image = self.attack_frames[self.current_attack_frame]
#                 old_center = self.rect.center
#                 self.rect = self.image.get_rect()
#                 self.rect.center = old_center
#                 self.hit_rect.centerx = self.pos.x
#                 self.hit_rect.centery = self.pos.y
#                 self.rect.center = self.hit_rect.center
                    

#         elif self.state == 'special':
#             if now - self.last_update > self.special_frame_rate:
#                 self.last_update = now
#                 if self.current_special_frame == 6:
#                     self.special()
#                 if self.current_special_frame < len(self.special_frames):
#                     self.image = self.special_frames[self.current_special_frame]
#                     self.current_special_frame += 1
#                 else:
#                     self.state = 'idle'
#                     self.current_special_frame = 0
#         elif self.state == 'hurt':
#             if now - self.last_update > self.frame_rate:
#                 self.last_update = now
#                 self.current_hurt_frame += 1
#                 if self.current_hurt_frame >= len(self.hurt_frames):
#                     self.state = 'idle'
#                     self.current_hurt_frame = 0
#                 self.image = self.hurt_frames[self.current_hurt_frame]
#                 old_center = self.rect.center
#                 self.rect = self.image.get_rect()
#                 self.rect.center = old_center
#                 self.hit_rect.centerx = self.pos.x
#                 self.hit_rect.centery = self.pos.y
#                 self.rect.center = self.hit_rect.center

#         if self.state not in ('attack', 'hurt', 'special'):
          
#             if self.state == 'walk':
#                 frames = self.walk_frames
#                 current_frame = self.current_walk_frame
#             else: 
#                 frames = self.animation_frames
#                 current_frame = self.current_frame

   
#             if now - self.last_update > self.frame_rate:
#                 self.last_update = now
#                 current_frame = (current_frame + 1) % len(frames)
#                 self.image = frames[current_frame]
                
    
#                 if self.state == 'walk':
#                     self.current_walk_frame = current_frame
#                 else:
#                     self.current_frame = current_frame
                
 
#                 old_center = self.rect.center
#                 self.rect = self.image.get_rect()
#                 self.rect.center = old_center
#                 self.hit_rect.centerx = self.pos.x
#                 self.hit_rect.centery = self.pos.y
#                 self.rect.center = self.hit_rect.center

        
#         self.pos += self.vel * dt
#         self.hit_rect.centerx = self.pos.x
#         collision(self, self.game_walls, 'x')
#         self.hit_rect.centery = self.pos.y
#         collision(self, self.game_walls, 'y')
#         self.rect.center = self.hit_rect.center

#     def rotate_image(self, direction):

#         flip = direction in ['left', 'up_left', 'down_left']
        
#         self.animation_frames = [
#             pygame.transform.flip(img, flip, False) 
#             for img in self.original_idle
#         ]
        
#         self.walk_frames = [
#             pygame.transform.flip(img, flip, False)
#             for img in self.original_walk
#         ]
        
#         self.attack_frames = [
#             pygame.transform.flip(img, flip, False)
#             for img in self.original_attack
#         ]

#         self.hurt_frames = [
#             pygame.transform.flip(img, flip, False)
#             for img in self.original_hurt
#         ]
        
#         self.special_frames = [
#             pygame.transform.flip(img, flip, False)
#             for img in self.original_special
#         ]
        
 
#         if self.state == 'walk':
#             self.image = self.walk_frames[self.current_walk_frame]
#         elif self.state == 'ice_attack':
#             self.image = self.attack_frames[self.current_attack_frame]
#         elif self.state == 'hurt':
#             self.image = self.hurt_frames[self.current_hurt_frame]
#         elif self.state == 'special':
#             if self.current_special_frame < len(self.special_frames):
#                 self.image = self.special_frames[self.current_special_frame]
#             else:
#                 self.image = self.special_frames[0] if self.special_frames else self.image
#         else:
#             self.image = self.animation_frames[self.current_frame]
      
#         old_center = self.rect.center
#         self.rect = self.image.get_rect()
#         self.rect.center = old_center
#         self.hit_rect.center = self.rect.center

        

# class Arrow(pygame.sprite.Sprite):
#     def __init__(self, x, y, player, direction):
#          pygame.sprite.Sprite.__init__(self)
#          self.player = player
#          self.original_image = player.assets['archer_flecha'][0]
#          self.image = self.rotate_image(direction)
#          self.all_skeletons = player.all_skeletons
#          self.rect = self.image.get_rect()
#          self.hit_rect = ARROW_HIT_RECT.copy()
#          self.rect.center = (x, y)
#          self.hit_rect.center = self.rect.center
#          self.speed = 500
#          self.direction = direction
#          self.vx, self.vy = self.get_velocity_vector(direction)
#          self.damaged_enemies = set()
#     def rotate_image(self, direction):
#          if direction == 'up':
#              return pygame.transform.rotate(self.original_image, 90)
#          elif direction == 'down':
#              return pygame.transform.rotate(self.original_image, -90)
#          elif direction == 'left':
#              return pygame.transform.rotate(self.original_image, 180)
#          elif direction == 'right':
#              return pygame.transform.rotate(self.original_image, 0)
#          elif direction == 'up_left':
#              return pygame.transform.rotate(self.original_image, 135)
#          elif direction == 'up_right':
#              return pygame.transform.rotate(self.original_image, 45)
#          elif direction == 'down_left':
#              return pygame.transform.rotate(self.original_image, -135)
#          elif direction == 'down_right':
#              return pygame.transform.rotate(self.original_image, -45)
#     def get_velocity_vector(self, direction):
#          if direction == 'up':
#              return (0, -1)
#          elif direction == 'down':
#              return (0, 1)
#          elif direction == 'left':
#              return (-1, 0)
#          elif direction == 'right':
#              return (1, 0)
#          elif direction == 'up_left':
#              return (-0.707, -0.707)
#          elif direction == 'up_right':
#              return (0.707, -0.707)
#          elif direction == 'down_left':
#              return (-0.707, 0.707)
#          elif direction == 'down_right':
#              return (0.707, 0.707)
#     def update(self, dt):
#         self.rect.x += self.vx * self.speed * dt
#         self.rect.y += self.vy * self.speed * dt

#         self.hit_rect.center = self.rect.center

#         # Check for collision with walls
#         hits = pygame.sprite.spritecollide(self, self.all_skeletons, False, collide_hit_rect)
#         for skeleton in hits:
#             if skeleton not in self.damaged_enemies:
#                 skeleton.health -= KNIGHT_ATTACK_DMG
#                 # Aplica o estado 'hurt' apenas se não for EliteOrc em attack2
#                 if isinstance(skeleton, EliteOrc):
#                     if skeleton.state != 'attack2':
#                         skeleton.state = 'hurt'
#                 elif not isinstance(skeleton, Necromancer):
#                     skeleton.state = 'hurt'
#                 self.damaged_enemies.add(skeleton)
#         #Se a flecha collidir com uma parede, ela desaparece.
#         for wall in self.player.game_walls:
#             if pygame.sprite.collide_rect(self, wall):
#                 self.kill()

         

    

                

