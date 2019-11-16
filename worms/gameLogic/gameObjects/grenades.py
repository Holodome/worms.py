import math
import random

from engine import Loader
from .physicsObject import PhysicsObject

GRENADE_OFFSET = 5, 5


class Grenade(PhysicsObject):
    IMAGE = Loader.get_image("grenade")

    def __init__(self, alive_sec, x, y):
        super().__init__(x, y, 5, 0.5, bounce_times=3, time_to_death_millis=alive_sec * 1000)

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), 15, 45, 2)

    def get_draw_position(self):
        return self._pos - GRENADE_OFFSET


class ClusterBomb(PhysicsObject):
    IMAGE = Loader.get_image("cluster_bomb")

    EXPLOSION_RADIUS = 10

    def __init__(self, alive_sec, x, y):
        super().__init__(x, y, 5, 0.5, bounce_times=3, time_to_death_millis=alive_sec * 1000)

    def get_draw_position(self):
        return self._pos - GRENADE_OFFSET

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), ClusterBomb.EXPLOSION_RADIUS, 10, 1)
        for _ in range(random.randrange(7, 10)):
            angle = random.random() * math.pi * 2
            cluster = Cluster(*self._pos)
            cluster.vel_x = math.cos(angle) * ClusterBomb.EXPLOSION_RADIUS
            cluster.vel_y = math.sin(angle) * ClusterBomb.EXPLOSION_RADIUS
            world.physicsObjects.append(cluster)


class Cluster(PhysicsObject):
    IMAGE = Loader.get_image("cluster")

    CLUSTER_OFFSET = 2, 2

    def __init__(self, x, y):
        super().__init__(x, y, 1, 0.8, bounce_times=1, time_to_death_millis=3000)

    def get_draw_position(self):
        return self._pos - Cluster.CLUSTER_OFFSET

    def death_action(self, world):
        world.explosion(int(self.x), int(self.y), 5, 7, 1)
