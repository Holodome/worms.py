from typing import List

import pygame

from engine import Color, Rect, Renderer
from .element import Element


class Container(Element):
    def __init__(self, rect=None):
        Element.__init__(self)
        self._color = Color(255, 255, 255, 0)
        if rect is not None:
            self._rect = rect

        self._image: pygame.Surface = None
        self.apply_rect()

        self._elements: List[Element] = []

    def on_update(self):
        for element in self._elements:
            element.on_update()

    def on_render(self):
        if not self._visible:
            return

        Renderer.submit((self._image, self._rect.topleft), False)
        for element in self._elements:
            element.on_render()

    def on_event(self, event):
        for element in self._elements:
            element.on_event(event)

    def add_element(self, element: Element):
        self._elements.append(element)
        element.constraints.update_rect(self._rect, element._rect)
        element.apply_rect()

        if isinstance(element, Container):
            for el in element._elements:
                el.constraints.update_rect(element._rect, el._rect)
                el.apply_rect()

    def set_color(self, color: Color):
        self._color = color
        self._image.fill(self._color)

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

    def set_rect(self, rect: Rect):
        self._rect = rect
        self.apply_rect()
        for element in self._elements:
            element.constraints.update_rect(self._rect, element._rect)
            element.apply_rect()
