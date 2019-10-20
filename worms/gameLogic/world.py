from typing import *

import pygame

from .terrain import Terrain


class World:
    def __init__(self, name: str, width: int, height: int,
                 background: pygame.Surface, foreground: pygame.Surface):
        self.name: str = name
        self.terrain: Terrain = Terrain(width, height, foreground)

        self.entities: List[object] = []

        self.backgroundImage: pygame.Surface = background

    def on_update(self):
        for _ in range(6):
            pass

    def on_render(self):
        pass
