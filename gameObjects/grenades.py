import random

from toolbox import loader
from .physicsObject import *

grenade_image = loader.get_image("grenade")
cluster_grenade_image = loader.get_image("cluster_bomb")
cluster_image = loader.get_image("cluster")


class Grenade(PhysicsObject):
    def __init__(self, alive_sec, x, y, vel_x, vel_y):
        super().__init__(x, y, 5, 0.5, 3, time_to_death=alive_sec)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        draw_position = self.position + offset - (5, 5)
        screen.blit(grenade_image, draw_position)

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), 15, 45, 2)


class ClusterBomb(PhysicsObject):
    def __init__(self, alive_sec, x, y, vel_x, vel_y):
        super().__init__(x, y, 5, 0.5, 3, time_to_death=alive_sec)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        draw_position = self.position + offset - (5, 5)
        screen.blit(cluster_grenade_image, draw_position)

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), 10, 10, 1)
        for _ in range(7):
            angle = random.random() * math.pi * 2
            world.entities.append(Cluster(*self.position, math.cos(angle) * 10, math.sin(angle) * 10))


class Cluster(PhysicsObject):
    def __init__(self, x: float, y: float, vel_x, vel_y):
        super().__init__(x, y, 1, 0.8, 1)
        self.velocity += (vel_x, vel_y)

    def draw(self, screen: pygame.Surface, offset: tuple):
        screen.blit(pygame.transform.rotate(cluster_image, math.degrees(self.angle)), self.position + offset - (2, 2))

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), 5, 7, 1)
