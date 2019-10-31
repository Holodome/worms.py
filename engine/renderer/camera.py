from typing import Union

import pygame

import engine.utils as utils
from ..input import Input
from ..types import Vector2


class Camera:
    CAMERA_SPEED = 0.5

    def __init__(self):
        self.pos: Vector2 = Vector2()

    def translate(self, a: Union[float, Vector2], y: float = 0) -> None:
        if isinstance(a, Vector2):
            self.pos += a
        else:
            self.pos.x += a
            self.pos.y += y

    def set_translation(self, a: Union[float, Vector2], y: float = 0) -> None:
        if isinstance(a, Vector2):
            self.pos = a
        else:
            self.pos.x = a
            self.pos.y = y

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, v):
        self.pos.x = v

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, v):
        self.pos.y = v

    @property
    def negative_translation(self):
        return tuple(map(int, -self.pos))


class CameraController:
    def __init__(self):
        self.camera: Camera = Camera()

    def on_update(self, timestep):
        if Input.is_key_pressed(pygame.K_a):
            self.camera.pos.x -= Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_d):
            self.camera.pos.x += Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_w):
            self.camera.pos.y -= Camera.CAMERA_SPEED * int(timestep)
        if Input.is_key_pressed(pygame.K_s):
            self.camera.pos.y += Camera.CAMERA_SPEED * int(timestep)

    def on_event(self, event):
        pass

    def clamp_position(self, x0, y0, x1, y1):
        self.camera.x = utils.clamp(self.camera.x, x0, x1, )
        self.camera.y = utils.clamp(self.camera.y, y0, y1, )
