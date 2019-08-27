import os
import random

from .physicsObject import *


class Grenade(PhysicsObject):
    image = pygame.image.load(os.path.join("res/images/grenade.png"))
    image.convert()

    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y, 5, 0.5, 3)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        draw_position = self.position + offset - (5, 5)
        screen.blit(self.image, draw_position)

    def bounce_death_action(self, world):
        world.explosion(int(self.x), int(self.y), 15)


class ClusterBomb(PhysicsObject):
    image = pygame.image.load(os.path.join("res/images/cluster_bomb.png"))
    image.convert()

    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y, 5, 0.5, 3)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        draw_position = self.position + offset - (5, 5)
        screen.blit(self.image, draw_position)

    def bounce_death_action(self, world):
        world.explosion(int(self.x), int(self.y), 10)
        for _ in range(15):
            angle = random.random() * math.pi * 2
            world.entities.append(Cluster(*self.position, math.cos(angle) * 10, math.sin(angle) * 10))


class Cluster(PhysicsObject):
    image = pygame.image.load(os.path.join("res/images/cluster.png"))
    image.convert()

    def __init__(self, x: float, y: float, vel_x, vel_y):
        super().__init__(x, y, 1, 0.8, 1)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        screen.blit(pygame.transform.rotate(self.image, math.degrees(self.angle)), self.position + offset - (2, 2))

    def bounce_death_action(self, world):
        world.explosion(int(self.x), int(self.y), 5)
