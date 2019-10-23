from typing import Union

import pygame

import engine.utils as utils
from engine.input import Input


class Camera:
    CAMERA_SPEED = 0.5

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

    def _set_x(self, v):
        self.position.x = v

    def _set_y(self, v):
        self.position.y = v

    def _get_x(self):
        return self.position.x

    def _get_y(self):
        return self.position.y

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

    @property
    def negative_translation(self):
        return tuple(map(int, -self.position))


class CameraController:
    def __init__(self):
        self.camera: Camera = Camera()

    def on_update(self, timestep):
        if Input.is_key_pressed(pygame.K_a):
            self.camera.position.x -= Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_d):
            self.camera.position.x += Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_w):
            self.camera.position.y -= Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_s):
            self.camera.position.y += Camera.CAMERA_SPEED * int(timestep)

    def on_event(self, event):
        pass

    def clamp_position(self, x0, y0, x1, y1):
        self.camera.x = utils.clamp(self.camera.x,x0, x1, )
        self.camera.y = utils.clamp(self.camera.y,y0, y1, )
