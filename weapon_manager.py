import math

import pygame

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


weapons = [Weapon(Grenade, loader.get_image("grenade")), Weapon(ClusterBomb, loader.get_image("cluster_bomb"))]


class WeaponManager:
    def __init__(self):
        self.weapons_quantity: dict = {w_id: -1 for w_id in weapon_ids}
        self.selected_weapon: int = 1

        self.shootingAngle = -math.pi / 4
        self.time = 3

    def fire(self, x, y, throw_force) -> list:
        assert throw_force != -1
        weapon = weapons[self.selected_weapon]
        weapon_id = weapon_ids[self.selected_weapon]
        if weapon_id == GRENADE or weapon_id == CLUSTER_BOMB:
            b = weapon.fire(self.time, x, y,
                            math.cos(self.shootingAngle) * throw_force * 50,
                            math.sin(self.shootingAngle) * throw_force * 50)
            return [b]

    def draw_menu(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        image = pygame.Surface((screen_width, screen_height * 2 // 5 + 1), pygame.SRCALPHA)
        image.fill((40, 40, 40, 230))
        screen.blit(image, (0, screen_height * 3 // 5))
