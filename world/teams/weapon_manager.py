import math

import pygame

from gameObjects import *
from toolbox import loader

GRENADE = 0x00
CLUSTER_BOMB = 0x01
DYNAMITE = 0x02
MINIGUN = 0x03
UZI = 0x04

weapon_ids = [GRENADE, CLUSTER_BOMB]


class Weapon:
    def __init__(self, bullet, worm_hold_image):
        self.bullet = bullet
        self.worm_hold_image = worm_hold_image

    def fire(self, _, x, y, vel_x, vel_y):
        return self.bullet(_, x, y, vel_x, vel_y)


weapons = [Weapon(Grenade, pygame.transform.scale2x(loader.get_image("grenade"))),
           Weapon(ClusterBomb, pygame.transform.scale2x(loader.get_image("cluster_bomb")))]


class WeaponManager:
    def __init__(self):
        self.weapons_quantity: dict = {w_id: -1 for w_id in weapon_ids}
        self.selected_weapon: int = CLUSTER_BOMB

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
        # TODO : draw using relative sizes
        image = pygame.Surface((screen_width, screen_height // 4), pygame.SRCALPHA)
        image.fill((40, 40, 40, 230))
        # 45 - square length, 10 on each side is padding
        # Draw selected time to detonation
        time_img = loader.get_font("RubberBiscuitBold.TTF", 20).render(str(self.time), False, (0, 150, 0, 245))
        image.blit(time_img, ((45 - time_img.get_width()) // 2 + 10, (45 - time_img.get_height()) // 2 + 10))
        # Draw selected weapon
        pygame.draw.rect(image, (100, 28, 52, 245), (10, 65, 45, 45))
        image.blit(weapons[self.selected_weapon].worm_hold_image,
                   (10 + (45 - weapons[self.selected_weapon].worm_hold_image.get_width()) // 2,
                    65 + (45 - weapons[self.selected_weapon].worm_hold_image.get_height()) // 2))
        # Draw all possible weapons
        for i, weapon in enumerate(weapons):
            x = i // 2 * 55 + 55
            y = 55 if (i + 1) % 2 == 0 else 0
            pygame.draw.rect(image, (20, 20, 20, 245), (x + 10, y + 10, 45, 45))
            image.blit(weapon.worm_hold_image, (x + 10 + (45 - weapon.worm_hold_image.get_width()) // 2,
                                                y + 10 + (45 - weapon.worm_hold_image.get_height()) // 2))

        screen.blit(image, (0, screen_height * 3 // 4))

    def select_weapon(self, mx: int, my: int, screen_height: int):
        mx -= 65
        my -= screen_height * 3 // 4 + 10
        for i, _ in enumerate(weapons):
            x = i // 2 * 55
            y = 55 if (i + 1) % 2 == 0 else 0
            if pygame.Rect(x, y, 45, 45).collidepoint(mx, my):
                self.selected_weapon = i
                return
