from typing import Union

import pygame

from ..types import Vector2


class Entity:
    Alive: bool = True

    __slots__ = ["image", "_pos"]

    def __init__(self, image: pygame.Surface, position: Vector2):
        self.image: pygame.Surface = image
        self._pos: Vector2 = position

    @property
    def pos(self) -> Vector2:
        return self._pos

    @pos.setter
    def pos(self, a: Union[Vector2, float], y: float = 0):
        if isinstance(a, Vector2):
            self._pos = a
        else:
            self._pos = Vector2(a, y)

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, v):
        self._pos.x = v

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, v):
        self._pos.y = v
