import pygame

from engine import Renderer
from .element import Element


class Label(Element):
    def __init__(self, image: pygame.Surface):
        Element.__init__(self)

        self._image = image
        self._rect = image.get_rect()

    def set_image(self, img):
        self._image = img
        self.apply_rect()

    def on_update(self):
        pass

    def on_render(self):
        Renderer.submit((self._image, self._rect.topleft), False)

    def on_event(self, event):
        pass

    def apply_rect(self):
        self._image = pygame.transform.scale(self._image, self._rect.size)

    def set_visible(self, visible: bool):
        super().set_visible(visible)
