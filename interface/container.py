from typing import List

import pygame

from .element import Element


class Container(Element):
    def __init__(self, rect=None):
        Element.__init__(self)
        self._color = pygame.Color(255, 255, 255, 255)
        if rect is not None:
            self._rect = rect

        self._image = None
        self.apply_rect()

        self._elements: List[Element] = []

    def on_update(self):
        for element in self._elements:
            element.on_update()

    def on_render(self, surface: pygame.Surface):
        assert self._image is not None, "Image not initialized"
        if not self._visible:
            return

        surface.blit(self._image, (0, 0))
        for element in self._elements:
            element.on_render(surface)

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
