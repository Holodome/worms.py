import pygame
from pygame import Vector2


class PhysicsObject:
    """
    All physics objects are represented as circles
    with certain radius and position

    """
    COLORKEY = (255, 0, 255)

    def __init__(self, x: float, y: float, radius: float, friction: float, bounce_times: int = -1):
        # Linear attributes
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.acceleration = Vector2()
        # Radius of the representing circle
        self.radius = radius
        # How much energy is saved after collision (0.0 - 1.0)
        self.friction = friction
        # How many times ball can bounce before some death action
        self.bounceTimes = bounce_times

    def bounce_death_action(self):
        raise NotImplementedError()

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

