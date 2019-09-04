import pygame
import math
import loader
from gameObjects import *

GRENADE = 0b00001
CLUSTER_BOMB = 0b00010
DYNAMITE = 0b00100
MINIGUN = 0b01000
UZI = 0b10000

weapon_ids = [GRENADE, CLUSTER_BOMB]


class Weapon:
    def __init__(self, bullet, worm_hold_image):
        self.bullet = bullet
        self.worm_hold_image = worm_hold_image

    def fire(self, _, x, y, vel_x, vel_y):
        return self.bullet(_, x, y, vel_x, vel_y)


weapons = [Weapon(Grenade, loader.get_image("grenade")), Weapon(CLUSTER_BOMB, loader.get_image("cluster_bomb"))]


class WeaponManager:
    def __init__(self):
        self.weapons_quantity: dict = {w_id: -1 for w_id in weapon_ids}
        self.selected_weapon: int = 0

        self.shootingAngle = -math.pi / 4
        self.time = 3

    def fire(self, world, throw_force) -> list:
        print(throw_force)
        weapon = weapons[self.selected_weapon]
        weapon_id = weapon_ids[self.selected_weapon]
        if weapon_id == GRENADE or weapon_id == CLUSTER_BOMB:
            b = weapon.fire(self.time, *world.selected_team.selected_worm.position,
                                              math.cos(self.shootingAngle) * throw_force * 50,
                                              math.sin(self.shootingAngle) * throw_force * 50)
            return [b]

    def draw_menu(self, screen: pygame.Surface):
        pass
