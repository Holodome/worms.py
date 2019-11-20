from typing import List

from engine import Loader
from .physicsObject import PhysicsObject, PhysicsObjectType


class Bullet(PhysicsObject):
    IMAGE = Loader.get_image("uzi_bullet")

    Type = PhysicsObjectType.Bullet

    def __init__(self, x: float, y: float, damage: int):
        super().__init__(x, y, 1, 1, 1, affected_by_gravity=0.1)

        self.damage: int = damage
        self.excludedEntities: List[PhysicsObject] = []

    def set_excluded_entities(self, entities):
        self.excludedEntities = entities

    def check_collisions(self, entities) -> bool:
        for worm in filter(lambda p: p.is_worm(), entities):
            if worm not in self.excludedEntities:
                if worm.pos.distance_to(self.pos) < worm.radius:
                    worm.health -= self.damage
                    worm.draw_health()
                    return True
        return False


class UziBullet(Bullet):
    IMAGE = Loader.get_image("uzi_bullet")

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 3)


class MinigunBullet(Bullet):
    IMAGE = Loader.get_image("minigun_bullet")

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 2)
