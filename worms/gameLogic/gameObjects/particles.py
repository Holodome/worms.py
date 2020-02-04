import pygame

from engine import Loader
from .physicsObject import PhysicsObject


class Debris(PhysicsObject):
    IMAGE = pygame.Surface((4, 2))
    IMAGE.fill((40, 40, 40))

    def __init__(self, x: float, y: float):
        PhysicsObject.__init__(self, x, y, 1,
                               0.8,
                               5, 5000)


class Blood(Debris):
    IMAGE = Loader.get_image("blood")
