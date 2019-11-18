import abc
import math
import random
from typing import (List, Type)

import pygame

from engine import Color, Loader, Rect, Vector2, Window
from interface import *
from worms.gameLogic.gameObjects.physicsObject import PhysicsObject
from .gameObjects.bullets import Bullet
from .gameObjects.grenades import ClusterBomb, Grenade


class FireData:
    """
    Класс, хранящий все данные о логике стрельбы, чтобы не засорять основной класс
    А также имеет несколько удобных функций
    """
    NO_FIRE = -1
    FIRE = 1

    ROT_SPEED = 0.002

    RADIUS = 40

    def __init__(self):
        self.throwForce: float = FireData.NO_FIRE
        self.angle: float = 0

        self.shooterPosition: Vector2 = Vector2(0)
        self.timeToExplode: int = 3

        self.fireWeapon: bool = False

    def reset(self):
        self.throwForce = FireData.NO_FIRE

        self.fireWeapon = False

    def get_offset(self):
        return math.cos(self.angle) * FireData.RADIUS, \
               math.sin(self.angle) * FireData.RADIUS

    def update_throw_force(self, delta):
        self.throwForce += delta
        if self.throwForce >= FireData.FIRE:
            self.fireWeapon = True

    def update_angle(self, clockwise: bool):
        if clockwise:
            self.angle += FireData.ROT_SPEED
        else:
            self.angle -= FireData.ROT_SPEED

    def reset_angle(self):
        self.angle = 0

    def is_fire(self):
        return self.fireWeapon

    def is_active(self):
        return self.throwForce != FireData.NO_FIRE


class AbstractWeapon(abc.ABC):
    HoldImage: pygame.Surface = None

    IsThrowable = False
    IsShooting = False

    def __init__(self):
        self.data: FireData = None

    def set_data(self, fire_data: FireData):
        """
        Вызывается при создании обеьекта - передача информации о стрельбе
        Поскольку она не будет изменяться в процессе стрельбы (механика)
        """
        self.data = fire_data

    @abc.abstractmethod
    def fire(self, world) -> None:
        """
        Функция, которая вызывается когда игрок стреляет
        Передается мир, в котором можно вызвать функции и добавить новые обьекты
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_valid(self) -> bool:
        """
        Проверка, что оружие закончило свою деятельность
        К примеру, гранату можно кинуть только один раз, после этого оружие удаляется
        А из Узи можно стрелять продолжительное время, поэтому нужна проверка
        """
        return False

    @abc.abstractmethod
    def update(self, dt: float) -> None:
        """
        Обновлние оружия
        В простом случае просто уменьшает время оставшейся стрельбы
        """
        raise NotImplementedError


class SimpleThrowable(AbstractWeapon, abc.ABC):
    IsThrowable = True

    def __init__(self, throwable: Type[PhysicsObject],
                 throw_force_coef: float):
        super().__init__()

        self.throwable: Type[PhysicsObject] = throwable
        self.throwForceCoef: float = throw_force_coef

        self._fired: bool = False

    def fire(self, world) -> None:
        bullet = self.throwable(self.data.timeToExplode, *self.data.shooterPosition)
        bullet.vel_x = math.cos(self.data.angle) * self.throwForceCoef * self.data.throwForce
        bullet.vel_y = math.sin(self.data.angle) * self.throwForceCoef * self.data.throwForce
        world.physicsObjects.add(bullet)

        self._fired = True

    def get_valid(self) -> bool:
        return not self._fired

    def update(self, dt: float) -> None:
        pass


class SimpleShooting(AbstractWeapon, abc.ABC):
    IsShooting = True

    def __init__(self, bullet: Type[PhysicsObject],
                 fire_times: int, time_between_fire_s: float, bullet_speed: float, max_angle_var: float):
        super().__init__()

        self.bullet = bullet
        self.fireTimes = fire_times
        self.timeBetweenFires: float = time_between_fire_s

        self.bulletSpeed: float = bullet_speed

        self.maxAngleVar: float = max_angle_var

        self.currentTimeLive = 0
        self.firedTimes = 0

    def fire(self, world) -> None:
        if not self.get_valid():
            return

        if self.currentTimeLive >= self.timeBetweenFires:
            self.currentTimeLive -= self.timeBetweenFires
            self.firedTimes += 1

            bullet = self.bullet(*self.data.shooterPosition)
            new_angle = self.data.angle + self.maxAngleVar * (random.random() * 2 - 1)
            bullet.vel_x = math.cos(new_angle) * self.bulletSpeed
            bullet.vel_y = math.sin(new_angle) * self.bulletSpeed
            world.physicsObjects.add(bullet)

    def update(self, dt: float) -> None:
        self.currentTimeLive += dt

    def get_valid(self) -> bool:
        return self.firedTimes < self.fireTimes


class WGrenade(SimpleThrowable):
    HoldImage = Loader.get_image("grenade")

    def __init__(self):
        super().__init__(Grenade, 40)


class WClusterBomb(SimpleThrowable):
    HoldImage = Loader.get_image("cluster_bomb")

    def __init__(self):
        super().__init__(ClusterBomb, 40)


class WUzi(SimpleShooting):
    HoldImage = Loader.get_image("uzi")

    def __init__(self):
        super().__init__(Bullet, 30, 0.1, 40, math.pi / 6)


# Weapon List - all weapon types have constructors with zero elements
Weapons: List[Type[AbstractWeapon]] = [
    WGrenade,
    WClusterBomb,
    WUzi
]


# Элемент интерфейса, предоставляющий выбор оружия
class SelectWeaponContainer(Container):
    def __init__(self):
        super().__init__(Rect(0, Window.Instance.height * 2 / 3, Window.Instance.width, Window.Instance.height / 3))
        self.set_color(Color(40, 40, 40, 230))

        self.title = Label(Loader.get_font("ALoveOfThunder.ttf", 200)
                           .render("WEAPONS", False, (180, 10, 0)))
        self.title.constraints.add_width_constraint(RelativeMultConstraint(0.25))
        self.title.constraints.add_height_constraint(AspectConstraint())
        self.title.constraints.add_x_constraint(RelativeMultConstraint(1))
        self.title.constraints.add_y_constraint(RelativeMultConstraint(1))
        self.add_element(self.title)

        self.weaponListContainer = Container()
        self.weaponListContainer.set_color(Color(35, 35, 35, 230))
        self.weaponListContainer.constraints.add_x_constraint(RelativeMultConstraint(1))
        self.weaponListContainer.constraints.add_y_constraint(RelativeMultConstraint(1.15))
        self.weaponListContainer.constraints.add_width_constraint(RelativeMultConstraint(1))
        self.weaponListContainer.constraints.add_height_constraint(RelativeMultConstraint(0.85))
        self.add_element(self.weaponListContainer)
        for i, weapon in enumerate(Weapons):
            weapon_img = weapon.HoldImage
            weapon_btn = Button(weapon_img)

            x = i // 2 * 0.05 + 0.05
            y = 0.5 if i % 2 == 1 else 0.1

            weapon_btn.constraints.add_x_constraint(RelativeAddConstraint(x))
            weapon_btn.constraints.add_y_constraint(RelativeAddConstraint(y))
            weapon_btn.constraints.add_width_constraint(RelativeMultConstraint(0.045))
            weapon_btn.constraints.add_height_constraint(AspectConstraint())
            self.weaponListContainer.add_element(weapon_btn)
