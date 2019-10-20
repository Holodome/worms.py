import pygame

from .element import Element


class Label(Element):
    def __init__(self, image: pygame.Surface):
        Element.__init__(self)

        self._image = image
        self._rect = image.get_rect()

    def on_update(self):
        pass

    def on_render(self, surface: pygame.Surface):
        surface.blit(self._image, self._rect)

    def on_event(self, event):
        pass

    def apply_rect(self):
        self._image = pygame.transform.scale(self._image, self._rect.size)

    def set_visible(self, visible: bool):
        super().set_visible(visible)
