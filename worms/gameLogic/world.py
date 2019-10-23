import math
import random
from typing import *

import pygame

from worms.gameLogic.gameObjects.debris import Debris
from .gameObjects.physicsObject import PhysicsCircleObject, PhysicsObject
from .terrain import Terrain


class World:
    GRAVITY = 1000

    def __init__(self, name: str, width: int, height: int,
                 background: pygame.Surface, foreground: pygame.Surface):
        self.name: str = name
        self.terrain: Terrain = Terrain(width, height, foreground)

        self.physicsObjects: List[PhysicsObject] = []

        self.backgroundImage: pygame.Surface = background

    def on_update(self, timestep):
        for _ in range(6):
            for pho in self.physicsObjects:
                if isinstance(pho, PhysicsCircleObject):
                    # Обновление времени жизни объекта
                    pho.timeToDeath -= int(timestep) / 6
                    # Гравитация
                    acc = World.GRAVITY * float(timestep)
                    pho.vel_y += acc * float(timestep)
                    # Позиция после гравитации
                    potential_pos = pho.position + pho.vel * float(timestep)
                    pho.stable = False
                    # Высчитывание вектора отражения
                    response = pygame.Vector2(0)
                    collided = False

                    times = 8
                    for r in map(lambda n: (n / times) * math.pi + (pho.angle - math.pi / 2.0), range(times)):
                        test_pos = pygame.Vector2(pho.radius * math.cos(r), pho.radius * math.sin(r)) + potential_pos
                        if self.terrain.valid_position(int(test_pos.x), int(test_pos.y)) \
                                and self.terrain.get_block_data(int(test_pos.x), int(test_pos.y)):
                            response += potential_pos - test_pos
                            collided = True
                    # Если объект столкунлся с землей - направить скорость в обратную сторону
                    if collided:
                        resp_mag = response.magnitude()
                        pho.stable = True
                        reflect = pho.vel_x * (response.x / resp_mag) + pho.vel_y * (response.y / resp_mag)
                        pho.vel = (pho.vel + (response / resp_mag * -2.0 * reflect)) * pho.friction
                        # Уменьшение числа оставшихся столкновений
                        if pho.bounceTimes != pho.INFINITE_BOUNCE:
                            pho.bounceTimes -= 1
                    else:
                        # Если столкновения не произошло - продолжить движение
                        pho.position = potential_pos

                    if not pho.is_valid():
                        # remove entity
                        pho.Alive = False
                    else:
                        if abs(pho.vel.magnitude()) < 0.001:
                            pho.stable = True
                            pho.vel -= pho.vel

            self.physicsObjects = list(filter(lambda p: p.Alive, self.physicsObjects))

    def explosion(self, x: int, y: int, radius: int, damage: int, force_coef: float):
        self.terrain.explode_circle(x, y, radius)
        for pho in self.physicsObjects:
            distance = pho.position.distance_to((x, y))
            if distance < radius:
                pho.stable = False
                angle = math.atan2(pho.y - y, pho.x - x)
                pho.vel += pygame.Vector2(math.cos(angle), math.sin(angle)) \
                           * force_coef * radius * ((radius - distance) / radius)
        for _ in range(radius // 2):
            angle = random.random() * math.pi * 2
            debris = Debris(x, y)
            debris.vel_x = math.cos(angle) * radius * 1.5
            debris.vel_y = math.sin(angle) * radius * 1.5
            self.physicsObjects.append(debris)
