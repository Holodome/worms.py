import pygame

from .physicsObject import PhysicsCircleObject


class Debris(PhysicsCircleObject):
    IMAGE = pygame.Surface((4, 2))
    IMAGE.fill((40, 40, 40))

    def __init__(self, x: float, y: float):
        PhysicsCircleObject.__init__(self, x, y, 1,
                                     0.8,
                                     5, 5000)
