import math
from typing import Tuple, Union

from engine import Entity, Renderer2D, Vector2, vec_to_itup


class PhysicsObject(Entity):
    IMAGE = None  # Инициализируется наследниками

    def __init__(self, x: float, y: float):
        Entity.__init__(self, self.IMAGE, Vector2(x, y))
        self._vel: Vector2 = Vector2(0.0)
        self.stable: bool = False

    def draw(self):
        Renderer2D.submit((self.image, vec_to_itup(self.pos)))

    @property
    def angle(self):
        return math.atan2(self._vel.y, self._vel.x)

    @property
    def vel_x(self):
        return self._vel.x

    @vel_x.setter
    def vel_x(self, v):
        self._vel.x = v

    @property
    def vel_y(self):
        return self._vel.y

    @vel_y.setter
    def vel_y(self, v):
        self._vel.y = v

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, a: Union[Vector2, Tuple[float, float], float], y: float = 0):
        if isinstance(a, Vector2):
            self._vel = a
        elif isinstance(a, tuple):
            self._vel = Vector2(a)
        else:
            self._vel = Vector2(a, y)


class PhysicsCircleObject(PhysicsObject):
    IMAGE = None

    INFINITE_BOUNCE = 1 << 31
    INFINITE_TIME = 1 << 31

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

    def death_action(self, world):
        pass
