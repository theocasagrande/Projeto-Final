import pygame
import os
from config import *
import random
from typing import List, Tuple
from pygame.locals import *
import pytmx

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append((line.strip()))
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = len(self.data[0]) * TILESIZE
        self.height = len(self.data) * TILESIZE

class TiledMap:
    def __init__(self, filename, scale):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.scale = scale
        self.width = self.tmxdata.width * self.tmxdata.tilewidth * scale
        self.height = self.tmxdata.height * self.tmxdata.tileheight * scale

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmxdata.tilewidth * self.scale, self.tmxdata.tileheight * self.scale))
                        surface.blit(tile, (x * self.tmxdata.tilewidth * self.scale,
                                            y * self.tmxdata.tileheight * self.scale))
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface