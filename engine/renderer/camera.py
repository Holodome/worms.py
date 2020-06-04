from typing import Union

import pygame

import engine.utils as utils
from .entity import Entity
from ..input import Input
from ..types import Vector2
from ..window import Window


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
        return utils.vec_to_itup(-self.pos)


class CameraController:
    def __init__(self):
        self.camera: Camera = Camera()

    def move(self, timestep) -> bool:
        moved = False
        if Input.is_key_held(pygame.K_a):
            self.camera.pos.x -= Camera.CAMERA_SPEED * int(timestep)
            moved = True
        if Input.is_key_held(pygame.K_d):
            self.camera.pos.x += Camera.CAMERA_SPEED * int(timestep)
            moved = True
        if Input.is_key_held(pygame.K_w):
            self.camera.pos.y -= Camera.CAMERA_SPEED * int(timestep)
            moved = True
        if Input.is_key_held(pygame.K_s):
            self.camera.pos.y += Camera.CAMERA_SPEED * int(timestep)
            moved = True
        return moved

    def on_event(self, event):
        pass

    def clamp_position(self, x0, y0, x1, y1):
        self.camera.x = utils.clamp(self.camera.x, x0, x1, )
        self.camera.y = utils.clamp(self.camera.y, y0, y1, )

    def center_to_entity(self, entity: Entity):
        self.camera.x = entity.x - Window.Instance.width / 2
        self.camera.y = entity.y - Window.Instance.height / 2
