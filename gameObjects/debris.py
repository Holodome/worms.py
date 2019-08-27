import math

import pygame

from .physicsObject import PhysicsObject


class Debris(PhysicsObject):
    image = pygame.Surface((4, 2))
    image.fill((40, 40, 40))

    def __init__(self, x: float, y: float, vel_x, vel_y):
        super().__init__(x, y, 1, 0.8, 5)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        screen.blit(pygame.transform.rotate(self.image, math.degrees(self.angle)), self.position + offset)
