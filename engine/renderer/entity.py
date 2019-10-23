import collections

import pygame

ComponentType = collections.namedtuple("ComponentType", ["name"])


class Entity:
    Alive: bool = True

    def __init__(self, image: pygame.Surface, position: pygame.Vector2):
        self.image: pygame.Surface = image
        self.position: pygame.Vector2 = position

    def set_position(self, x: float, y: float):
        self.position.x = x
        self.position.y = y

    def _set_x(self, v): self.position.x = v

    def _set_y(self, v): self.position.y = v

    def _get_x(self): return self.position.x

    def _get_y(self): return self.position.y

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
