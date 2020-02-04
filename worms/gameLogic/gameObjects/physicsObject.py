import enum
import math
from typing import Tuple, Union

from engine import Entity, Renderer, Vector2, vec_to_itup


class PhysicsObjectType(enum.Enum):
    Null = 0

    Normal = 1  # Обьект без особого поведения
    Worm = 2
    Bullet = 3  # Обьект, сталкивающийся с другими существами


class PhysicsObject(Entity):
    IMAGE = None  # Инициализируется наследниками

    INFINITE_BOUNCE = 1 << 31
    INFINITE_TIME = 1 << 31

    Type: PhysicsObjectType = PhysicsObjectType.Null  # Инициализируется наследниками

    __slots__ = ["_vel", "stable", "radius", "friction", "bounceTimes", "timeToDeath", "affectedByGravity"]

    @classmethod
    def is_worm(cls):
        return cls.Type == PhysicsObjectType.Worm

    @classmethod
    def is_bullet(cls):
        return cls.Type == PhysicsObjectType.Bullet

    def __init__(self, x: float, y: float, radius: float,
                 friction: float,
                 bounce_times: int = INFINITE_BOUNCE, time_to_death_millis: int = INFINITE_TIME,
                 affected_by_gravity: float = 1.0):
        super().__init__(self.IMAGE, Vector2(x, y))
        self._vel: Vector2 = Vector2(0.0)
        self.stable: bool = False

        self.radius: float = radius
        # Коофицент сохранения жнергии после сохранения
        self.friction: float = friction
        # Сколько раз обьект может сталкиваться и какое ограничение времени по жизни у него есть
        self.bounceTimes: int = bounce_times
        self.timeToDeath: int = time_to_death_millis

        self.affectedByGravity: float = affected_by_gravity

    def is_valid(self):
        return (self.bounceTimes == PhysicsObject.INFINITE_BOUNCE or self.bounceTimes > 0) and \
               (self.timeToDeath == PhysicsObject.INFINITE_TIME or self.timeToDeath > 0)

    def draw(self):
        Renderer.submit((self.image, self.get_draw_position()))

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

    def get_draw_position(self) -> Vector2:
        return self.pos

    def death_action(self, world):
        pass

    def decrease_bounce(self):
        if self.bounceTimes != PhysicsObject.INFINITE_BOUNCE:
            self.bounceTimes -= 1

    def set_response(self, response):
        resp_mag = response.magnitude()
        self.stable = True
        reflect = self.vel_x * (response.x / resp_mag) + self.vel_y * (response.y / resp_mag)
        self.vel = (self.vel + (response / resp_mag * -2.0 * reflect)) * self.friction
        self.decrease_bounce()

    def finish_update(self):
        if abs(self.vel.magnitude()) < 0.1:
            self.stable = True
            self.vel = Vector2(0, 0)

    def set_sample_times(self):
        return
