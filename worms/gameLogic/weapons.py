import abc
import math
from typing import (List, Type)

import pygame

from engine import Color, Loader, Rect, Vector2, Window
from interface import *
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

        self.shooter_position: Vector2 = Vector2(0)

        self.fireWeapon: bool = False

    def reset(self):
        self.throwForce = FireData.NO_FIRE
        # self.angle = 0

        self.fireWeapon = False

    def get_offset(self):
        return math.cos(self.angle) * FireData.RADIUS, \
               math.sin(self.angle) * FireData.RADIUS

    def update_throw_force(self, delta):
        self.throwForce += delta
        self.throwForce = min(self.throwForce, FireData.FIRE)

    def update_angle(self, clockwise: bool):
        if clockwise:
            self.angle += FireData.ROT_SPEED
        else:
            self.angle -= FireData.ROT_SPEED

    def reset_angle(self):
        self.angle = 0

    def is_fire(self):
        return self.throwForce >= FireData.FIRE or self.fireWeapon

    def is_active(self):
        return self.throwForce != FireData.NO_FIRE


class AbstractWeapon(abc.ABC):
    HoldImage: pygame.Surface = None

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
    def update(self, dt) -> None:
        """
        Обновлние оружия
        В простом случае просто уменьшает время оставшейся стрельбы
        """
        raise NotImplementedError


class SimpleThrowable(AbstractWeapon, abc.ABC):
    def __init__(self, throwable: type, throw_force_coef):
        super().__init__()

        self.throwable: type = throwable
        self.throwForceCoef = throw_force_coef

    def fire(self, world) -> None:
        bullet = self.throwable(5, *self.data.shooter_position)
        bullet.vel_x = math.cos(self.data.angle) * self.throwForceCoef * self.data.throwForce
        bullet.vel_y = math.sin(self.data.angle) * self.throwForceCoef * self.data.throwForce
        world.physicsObjects.append(bullet)

    def get_valid(self) -> bool:
        return False

    def update(self, dt) -> None:
        pass


class WGrenade(SimpleThrowable):
    HoldImage = Loader.get_image("grenade")

    def __init__(self):
        super().__init__(Grenade, 40)


class WClusterBomb(SimpleThrowable):
    HoldImage = Loader.get_image("cluster_bomb")

    def __init__(self):
        super().__init__(ClusterBomb, 40)


Weapons: List[Type[AbstractWeapon]] = [
    WGrenade
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
