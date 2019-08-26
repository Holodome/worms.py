import pygame
from pygame import Vector2
import math


class PhysicsObject:
    """
    All physics objects are represented as circles
    with certain radius and position

    """
    COLORKEY = (255, 0, 255)

    def __init__(self, x: float, y: float, radius: float, friction: float, bounce_times: int = -1):
        # Linear attributes
        self.position: Vector2 = Vector2(x, y)
        self.velocity: Vector2 = Vector2()
        self.acceleration: Vector2 = Vector2()

        self.stable: bool = False
        # Radius of the representing circle
        self.radius: float = radius
        # How much energy is saved after collision (0.0 - 1.0)
        self.friction: float = friction
        # How many times ball can bounce before some death action
        self.bounceTimes: int = bounce_times

    def bounce_death_action(self):
        raise NotImplementedError()

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def angle(self):
        return math.atan2(self.velocity.y, self.velocity.x)
