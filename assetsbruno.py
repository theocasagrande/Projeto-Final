import pygame
import os
import random
from pygame.locals import *
from typing import List, Tuple
from config import *

def load_arrow_image():
    arrow_img = pygame.image.load(os.path.join(IMG_DIR, 'Arrow02(32x32).png')).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (TILESIZE, TILESIZE))
    return arrow_img

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, arrow_img):
        super().__init__()
        self.original_image = arrow_img
        self.image = self.rotate_image(direction)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 100
        self.direction = direction
        self.vx, self.vy = self.get_velocity_vector(direction)
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