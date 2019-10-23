import math
from typing import Union

import pygame

from engine.renderer.entity import Entity


class PhysicsObject(Entity):
    IMAGE = None  # Инициализируется наследниками

    def __init__(self, x: float, y: float):
        Entity.__init__(self, self.IMAGE, pygame.Vector2(x, y))

        self._velocity: pygame.Vector2 = pygame.Vector2(0.0)
        self.stable: bool = False

    def _get_velocity(self):
        return self._velocity

    def _set_velocity(self, a: Union[pygame.Vector2, float], y: float = 0):
        if isinstance(a, pygame.Vector2):
            self._velocity = a
        else:
            self._velocity = pygame.Vector2(a, y)

    def _get_velocity_x(self):
        return self._velocity.x

    def _get_velocity_y(self):
        return self._velocity.y

    def _set_velocity_x(self, v: float):
        self._velocity.x = v

    def _set_velocity_y(self, v: float):
        self._velocity.y = v

    @property
    def angle(self):
        return math.atan2(self._velocity.y, self._velocity.x)

    vel_x = property(_get_velocity_x, _set_velocity_x)
    vel_y = property(_get_velocity_y, _set_velocity_y)
    vel = property(_get_velocity, _set_velocity)


class PhysicsCircleObject(PhysicsObject):
    IMAGE = None

    INFINITE_BOUNCE = -1 << 30
    INFINITE_TIME = -1 << 30

    def __init__(self, x: float, y: float, radius: float,
                 friction: float,
                 bounce_times: int = INFINITE_BOUNCE, time_to_death_millis: int = INFINITE_TIME):
        PhysicsObject.__init__(self, x, y)

        self.radius: float = radius
        # Коофицент сохранения жнергии после сохранения
        self.friction: float = friction
        # Сколько раз обьект может сталкиваться и какое ограничение времени по жизни у него есть
        self.bounceTimes: int = bounce_times
        self.timeToDeath: int = time_to_death_millis

    def is_valid(self):
        return self.bounceTimes == PhysicsCircleObject.INFINITE_BOUNCE or self.bounceTimes > 0 and \
               self.timeToDeath == PhysicsCircleObject.INFINITE_TIME or self.timeToDeath > 0
