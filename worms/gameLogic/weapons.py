import abc
import math
import random
from typing import (List, Type)

import pygame

from engine import Color, Loader, Rect, Vector2, Window
from engine.renderer.renderer import Renderer
from interface import *
from worms.gameLogic.gameObjects.physicsObject import PhysicsObject
from .gameObjects.bullets import Bullet, MinigunBullet, SniperBullet, UziBullet
from .gameObjects.grenades import ClusterBomb, Grenade


class FireData:
    """
    Класс, хранящий все данные о логике стрельбы, чтобы не засорять основной класс
    А также имеет несколько удобных функций
    """
    # Параметры силы стрельбы
    NO_FIRE = -1
    FIRE = 1
    # Скорость вращения прицела
    ROT_SPEED = 0.01
    # Радиус прицела
    RADIUS = 40

    def __str__(self):
        return f""" FireData
    throwForce: {self.throwForce}
    angle: {self.angle}
    shooterPos: {self.shooterPosition}
    timeToExplode: {self.timeToExplode}
    fireWeapon: {self.fireWeapon}
    """

    def __init__(self):
        self.throwForce: float = FireData.NO_FIRE
        self.angle: float = 0

        self.shooterPosition: Vector2 = Vector2(0)
        self.timeToExplode: int = 3

        self.fireWeapon: bool = False
        # ОбЪекты, которые должны быть проигнорированные при проверке столкновений
        self.excludedEntities: List[PhysicsObject] = []

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
        self.angle %= math.pi * 2

    def reset_angle(self):
        self.angle = 0

    def is_fire(self) -> bool:
        return self.fireWeapon

    def end_fire(self):
        self.fireWeapon = False

    def is_active(self):
        return self.throwForce != FireData.NO_FIRE


class AbstractWeapon(abc.ABC):
    HoldImage: pygame.Surface = None
    # Определение типа оружия
    IsThrowable = False
    IsShooting = False

    data: FireData = FireData()

    @classmethod
    def draw_hold(cls):
        """
        Отрисовка оружия в руках червяка
        """
        raise NotImplementedError

    @classmethod
    def set_data(cls, fire_data: FireData):
        """
        Вызывается при создании обеьекта - передача информации о стрельбе
        Поскольку она не будет изменяться в процессе стрельбы (механика)

        Метод статический, поскольку одновременно может существовать только одна FireData
        """
        cls.data = fire_data

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


SetData = AbstractWeapon.set_data


class SimpleThrowable(AbstractWeapon, abc.ABC):
    IsThrowable = True

    @classmethod
    def draw_hold(cls):
        Renderer.submit((pygame.transform.rotate(cls.HoldImage, math.degrees(-cls.data.angle) - 90),
                         cls.data.shooterPosition - (3, 3)))

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
        world.physicsObjects.append(bullet)

        self._fired = True

    def get_valid(self) -> bool:
        return not self._fired

    def update(self, dt: float) -> None:
        pass


class SimpleShooting(AbstractWeapon, abc.ABC):
    IsShooting = True

    @classmethod
    def draw_hold(cls):
        image = cls.HoldImage
        # Переворот изображения при стрельбе в другую сторону
        if not (0 < cls.data.angle < math.pi / 2 or 1.5 * math.pi < cls.data.angle < math.pi * 2):
            image = pygame.transform.flip(image, False, True)
        Renderer.submit((pygame.transform.rotate(image, math.degrees(-cls.data.angle)),
                         cls.data.shooterPosition - (3, 3)))

    def __init__(self, bullet: Type[Bullet],
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
            bullet.set_excluded_entities(self.data.excludedEntities)
            new_angle = self.data.angle + self.maxAngleVar * (random.random() * 2 - 1)
            bullet.vel_x = math.cos(new_angle) * self.bulletSpeed
            bullet.vel_y = math.sin(new_angle) * self.bulletSpeed
            world.physicsObjects.append(bullet)

    def update(self, dt: float) -> None:
        self.currentTimeLive += dt

    def get_valid(self) -> bool:
        return self.firedTimes < self.fireTimes


class WGrenade(SimpleThrowable):
    HoldImage = Loader.get_image("grenade")

    def __init__(self):
        super().__init__(Grenade, 60)


class WClusterBomb(SimpleThrowable):
    HoldImage = Loader.get_image("cluster_bomb")

    def __init__(self):
        super().__init__(ClusterBomb, 60)


class WUzi(SimpleShooting):
    HoldImage = Loader.get_image("uzi")

    def __init__(self):
        super().__init__(UziBullet, 50, 0.06, 80, math.pi / 4)


class WMinigun(SimpleShooting):
    HoldImage = Loader.get_image("minigun")

    def __init__(self):
        super().__init__(MinigunBullet, 50, 0.03, 50, math.pi / 5)


class WSniper(SimpleShooting):
    HoldImage = Loader.get_image("sniper")

    def __init__(self):
        super().__init__(SniperBullet, 1, 1, 150, 0)


# Weapon List - all weapon types have constructors with zero elements
Weapons: List[Type[AbstractWeapon]] = [
    WGrenade,
    WClusterBomb,
    WUzi,
    WMinigun,
    WSniper
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
            weapon_img = weapon.HoldImage.copy()
            pygame.draw.rect(weapon_img, (255, 0, 0), weapon_img.get_rect(), 1)
            weapon_btn = Button(weapon_img)

            x = i // 2 * 0.05 + 0.15
            y = 0.5 if i % 2 == 1 else 0.1

            weapon_btn.constraints.add_x_constraint(RelativeAddConstraint(x))
            weapon_btn.constraints.add_y_constraint(RelativeAddConstraint(y))
            weapon_btn.constraints.add_width_constraint(RelativeMultConstraint(0.045))
            weapon_btn.constraints.add_height_constraint(AspectConstraint())
            weapon_btn.set_click_function(self.set_id_wrapper(i))
            self.weaponListContainer.add_element(weapon_btn)

        self.explodeTimeLabel = Label(Loader.get_font("ALoveOfThunder.ttf", 200)
                                      .render("3", False, (180, 10, 0)))
        self.explodeTimeLabel.constraints.add_x_constraint(RelativeAddConstraint(0.05))
        self.explodeTimeLabel.constraints.add_y_constraint(RelativeAddConstraint(0.1))
        self.explodeTimeLabel.constraints.add_width_constraint(RelativeMultConstraint(0.035))
        self.explodeTimeLabel.constraints.add_height_constraint(AspectConstraint())
        self.weaponListContainer.add_element(self.explodeTimeLabel)

        self.lastSelectedWeaponID = 0

    def set_time(self, time: int):
        assert 1 <= time <= 5
        self.explodeTimeLabel.set_image(Loader.get_font("ALoveOfThunder.ttf", 200)
                                        .render(str(time), False, (180, 10, 0)))

    def set_id_wrapper(self, i):
        return lambda _: setattr(self, "lastSelectedWeaponID", i)
