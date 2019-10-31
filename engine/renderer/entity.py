from typing import Union

import pygame
import engine

class Entity:
    Alive: bool = True

    def __init__(self, image: pygame.Surface, position: pygame.Vector2):
        self.image: pygame.Surface = image
        self._pos: pygame.Vector2 = position

    def simple_draw(self):
        engine.renderer.renderer2D.Renderer2D.submit((self.image, tuple(self.pos)))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, a: Union[pygame.Vector2, float], y: float = 0):
        if isinstance(a, pygame.Vector2):
            self._pos = a
        else:
            self._pos = pygame.Vector2(a, y)

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
