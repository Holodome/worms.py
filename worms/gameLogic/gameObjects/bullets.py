import math
import random
from typing import List

from engine import Loader
from worms.gameLogic.gameObjects.particles import Blood
from .physicsObject import PhysicsObject, PhysicsObjectType


class Bullet(PhysicsObject):
    IMAGE = Loader.get_image("uzi_bullet")

    Type = PhysicsObjectType.Bullet

    def __init__(self, x: float, y: float, damage: int):
        super().__init__(x, y, 1, 1, 1, time_to_death_millis=3000, affected_by_gravity=0.1)

        self.damage: int = damage
        self.excludedEntities: List[PhysicsObject] = []

        self.hitWorm = False

    def set_excluded_entities(self, entities):
        self.excludedEntities = entities

    def check_collisions(self, entities) -> bool:
        for worm in filter(lambda p: p.is_worm(), entities):
            if worm not in self.excludedEntities:
                if worm.pos.distance_to(self.pos) < worm.radius:
                    worm.health -= self.damage
                    worm.draw_health()
                    for i in range(10):
                        bl = Blood(*worm.pos)
                        angle = random.random() * math.pi * 2
                        bl.vel_x = math.cos(angle) * 10
                        bl.vel_y = math.sin(angle) * 10
                        entities.append(bl)
                    self.hitWorm = True
                    return True
        return False


class UziBullet(Bullet):
    IMAGE = Loader.get_image("uzi_bullet")

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 5)


class MinigunBullet(Bullet):
    IMAGE = Loader.get_image("minigun_bullet")

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 4)


class SniperBullet(Bullet):
    IMAGE = Loader.get_image("sniper_bullet")

    def __init__(self, x, y):
        super().__init__(x, y, 80)
