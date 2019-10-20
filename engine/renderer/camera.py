from typing import Union

import pygame


class Camera:

    def __init__(self):
        self.position: pygame.Vector2 = pygame.Vector2()

    def get_position(self) -> pygame.Vector2:
        return self.position

    def translate(self, a: Union[float, pygame.Vector2], y: float = 0) -> None:
        if isinstance(a, pygame.Vector2):
            self.position += a
        else:
            self.position.x += a
            self.position.y += y

    def set_translation(self, a: Union[float, pygame.Vector2], y: float = 0) -> None:
        if isinstance(a, pygame.Vector2):
            self.position = a
        else:
            self.position.x = a
            self.position.y = y


class CameraController:
    def __init__(self):
        self.camera: Camera = Camera()

    def on_update(self):
        pass

    def on_event(self, event):
        pass
