import math

import pygame


class PhysicsObject:
    """
    All physics objects are represented as circles
    with certain radius and position

    """
    COLORKEY = (255, 0, 255)
    font = pygame.font.SysFont("consolas", 10)  # Make font common for all inheritors

    def __init__(self, x: float, y: float, radius: float,
                 friction: float, bounce_times: int = -1, gravity: bool = True):
        # Linear attributes
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0)

        self.affectedByGravity = gravity

        self.stable: bool = False
        # Radius of the representing circle
        self.radius: float = radius
        # How much energy is saved after collision (0.0 - 1.0)
        self.friction: float = friction
        # How many times ball can bounce before some death action
        self.bounceTimes: int = bounce_times

    def draw(self, screen: pygame.Surface, offset: tuple):
        raise NotImplementedError()

    def bounce_death_action(self, world):
        """
        Override this function to add death action
        """
        pass

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def angle(self):
        return math.atan2(self.velocity.y, self.velocity.x)
