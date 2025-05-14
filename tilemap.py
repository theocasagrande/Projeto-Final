import pygame
import os
from config import *
import random
from typing import List, Tuple
from pygame.locals import *

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
