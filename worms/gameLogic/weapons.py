import math

import pygame

from engine import Color, Loader, Rect, Window
from interface import *


class Weapon:
    def __init__(self, w_id: int, bullet, hold_image: pygame.Surface):
        self.w_id = w_id

        self.bullet = bullet
        self.holdImage: pygame.Surface = hold_image


Weapons = [
    Weapon(0, Loader.get_image("grenade"), Loader.get_image("grenade")),
    Weapon(1, Loader.load_image("cluster_bomb"), Loader.load_image("cluster_bomb"))
]


class FireData:
    NO_FIRE = -1
    FIRE = 1

    ROT_SPEED = 0.002

    RADIUS = 40

    def __init__(self):
        self.throwForce: float = FireData.NO_FIRE
        self.angle: float = 0

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
        # TODO: Rework to manage pictures of different sizes
        for i, weapon in enumerate(Weapons):
            weapon_img = weapon.holdImage
            weapon_btn = Button(weapon_img)

            x = i // 2 * 0.05 + 0.05
            y = 0.5 if i % 2 == 1 else 0.1

            weapon_btn.constraints.add_x_constraint(RelativeAddConstraint(x))
            weapon_btn.constraints.add_y_constraint(RelativeAddConstraint(y))
            weapon_btn.constraints.add_width_constraint(RelativeMultConstraint(0.045))
            weapon_btn.constraints.add_height_constraint(AspectConstraint())
            self.weaponListContainer.add_element(weapon_btn)


class WeaponManager:
    def __init__(self):
        self.weaponCount = [-1 for _ in Weapons]
        self.selectedWeapon: int = 0

        self.timeToExplode: int = 3
