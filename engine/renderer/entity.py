import collections
from typing import Union

import pygame

ComponentType = collections.namedtuple("ComponentType", ["name"])


class Entity:
    Alive: bool = True

    def __init__(self, image: pygame.Surface, position: pygame.Vector2):
        self.image: pygame.Surface = image
        self._pos: pygame.Vector2 = position

    def _set_x(self, v): self._pos.x = v

    def _set_y(self, v): self._pos.y = v

    def _get_x(self): return self._pos.x

    def _get_y(self): return self._pos.y

    def _get_pos(self): return self._pos

    def _set_pos(self, a: Union[pygame.Vector2, float], y: float = 0):
        if isinstance(a, pygame.Vector2):
            self._pos = a
        else:
            self._pos = pygame.Vector2(a, y)

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    pos = property(_get_pos, _set_pos)
