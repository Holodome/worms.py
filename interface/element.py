import abc

import pygame

from .constraint import ConstraintManager


class Element:
    _rect: pygame.Rect = pygame.Rect(0, 0, 1, 1)

    def __init__(self):
        self._visible: bool = False
        # self.constraintManager = ConstraintManager()
        self.constraintManager = ConstraintManager()

    @abc.abstractmethod
    def on_update(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_render(self, surface: pygame.Surface):
        raise NotImplementedError

    @abc.abstractmethod
    def on_event(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def apply_rect(self):
        raise NotImplementedError

    def set_visible(self, visible: bool):
        self._visible = visible
