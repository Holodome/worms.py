from typing import List

from engine import Loader
from .physicsObject import PhysicsObject


class Bullet(PhysicsObject):
    IMAGE = Loader.get_image("uzi_bullet")

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 1, 1, 1, affected_by_gravity=0.1, collide_with_entities=True)

        self.damage: int = 3
        self.excludedEntities: List[PhysicsObject] = []
