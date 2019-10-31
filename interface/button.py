from typing import Callable

import pygame

from engine import Entity, Input, Renderer2D
from .element import Element


class Button(Element):
    def __init__(self, static_image: pygame.Surface, hovered_image: pygame.Surface = None):
        Element.__init__(self)

        if hovered_image is None:
            hovered_image = static_image

        self._staticImage: pygame.Surface = static_image
        self._hoveredImage: pygame.Surface = hovered_image

        self._rect = static_image.get_rect()

        self._hovered: bool = False

        self._clickFunction: Callable = lambda _: None

    def on_update(self):
        self._hovered = self._rect.collidepoint(*Input.get_mouse_pos())

    def on_render(self):
        if self._hovered:
            Renderer2D.submit_one(Entity(self._hoveredImage, self._rect.topleft))
        else:
            Renderer2D.submit_one(Entity(self._staticImage, self._rect.topleft))

    def on_event(self, dispatcher):
        if self._hovered:
            dispatcher.dispatch(pygame.MOUSEBUTTONUP, self._clickFunction)

    def apply_rect(self):
        self._staticImage = pygame.transform.scale(self._staticImage, self._rect.size)
        self._hoveredImage = pygame.transform.scale(self._hoveredImage, self._rect.size)

    def set_click_function(self, function: Callable):
        self._clickFunction = function
