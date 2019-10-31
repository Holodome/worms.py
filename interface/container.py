from typing import List

import pygame

from engine.renderer.entity import Entity
from engine.renderer.renderer2D import Renderer2D
from .element import Element


class Container(Element):
    def __init__(self, rect=None):
        Element.__init__(self)
        self._color = pygame.Color(255, 255, 255, 0)
        if rect is not None:
            self._rect = rect

        self._image: pygame.Surface = None
        self.apply_rect()

        self._elements: List[Element] = []

    def on_update(self):
        for element in self._elements:
            element.on_update()

    def on_render(self):
        assert self._image is not None, "Image not initialized"
        if not self._visible:
            return

        Renderer2D.submit_one(Entity(self._image, self._rect.topleft))
        for element in self._elements:
            element.on_render()

    def on_event(self, event):
        for element in self._elements:
            element.on_event(event)

    def add_element(self, element: Element):
        self._elements.append(element)
        element.constraintManager.update_rect(self._rect, element._rect)
        element.apply_rect()

    def set_color(self, color: pygame.Color):
        self._color = color

    def apply_rect(self):
        self._image = pygame.Surface(self._rect.size, pygame.SRCALPHA)
        self._image.fill(self._color)

    def set_all_visible(self):
        self._visible = True
        for element in self._elements:
            if isinstance(element, Container):
                element.set_all_visible()
            else:
                element.set_visible(True)

    def set_rect(self, rect: pygame.Rect):
        self._rect = rect
        self.apply_rect()
        for element in self._elements:
            element.constraintManager.update_rect(self._rect, element._rect)
            element.apply_rect()