import math
import random
from typing import *

import pygame

from engine import Renderer2D, Vector2
from .gameObjects.debris import Debris
from .gameObjects.physicsObject import PhysicsObject
from .gameObjects.worm import Worm
from .terrain import Terrain
from .wormsTeam import TeamManager

GRAVITY_ACC = 1000
MAX_DEBRIS_COUNT = 100


class World:

    def __init__(self, name: str, width: int, height: int,
                 background: pygame.Surface, foreground: pygame.Surface):
        self.name: str = name
        self.terrain: Terrain = Terrain(width, height, foreground)

        self.physicsObjects: Set[PhysicsObject] = set()

        self.backgroundImage: pygame.Surface = background

        self.teamManager: TeamManager = TeamManager()
        self.teamManager.set_team_positions(world_width=width)
        for team in self.teamManager.teams:
            for worm in team.wormList:
                self.physicsObjects.add(worm)

        self.debrisCount: int = 0

    def on_update(self, timestep):
        for _ in range(6):
            for ent in self.physicsObjects:
                # Обновление времени жизни объекта
                ent.timeToDeath -= int(timestep) / 6
                # Гравитация
                acc = GRAVITY_ACC * float(timestep) * ent.affectedByGravity
                ent.vel_y += acc * float(timestep)
                # Позиция после гравитации
                potential_pos = ent.pos + ent.vel * float(timestep)
                ent.stable = False
                # Высчитывание вектора отражения
                response = Vector2(0)
                collided = False

                times = 8
                for r in map(lambda n: (n / times) * math.pi + (ent.angle - math.pi / 2.0), range(times)):
                    test_pos = Vector2(ent.radius * math.cos(r), ent.radius * math.sin(r)) + potential_pos
                    if self.terrain.valid_position(int(test_pos.x), int(test_pos.y)) \
                            and self.terrain.get_block_data(int(test_pos.x), int(test_pos.y)):
                        response += potential_pos - test_pos
                        collided = True

                if not collided and ent.collideWithWorms:
                    for worm in filter(lambda p: isinstance(p, Worm), self.physicsObjects):
                        if worm is not ent:
                            if worm.pos.distance_to(ent.pos) < worm.radius:
                                collided = True
                                worm.health -= ent.damage
                                worm.draw_health()
                                response = potential_pos - test_pos
                                break

                # Если объект столкунлся с землей - направить скорость в обратную сторону
                if collided:
                    resp_mag = response.magnitude()
                    ent.stable = True
                    reflect = ent.vel_x * (response.x / resp_mag) + ent.vel_y * (response.y / resp_mag)
                    ent.vel = (ent.vel + (response / resp_mag * -2.0 * reflect)) * ent.friction
                    # Уменьшение числа оставшихся столкновений
                    if ent.bounceTimes != ent.INFINITE_BOUNCE:
                        ent.bounceTimes -= 1
                else:
                    # Если столкновения не произошло - продолжить движение
                    ent.pos = potential_pos

                if not ent.is_valid():
                    # remove entity
                    ent.Alive = False

                    # if isinstance(pho, Debris):
                    #     self.debrisCount -= 1
                else:
                    if abs(ent.vel.magnitude()) < 0.001:
                        ent.stable = True
                        ent.vel -= ent.vel

                    if isinstance(ent, Worm):
                        ent.headedRight = ent.vel_x > 0

            old = self.physicsObjects.copy()
            self.physicsObjects.clear()
            for p in old:
                if not (p.Alive and 0 <= p.x < self.terrain.width and 0 <= p.y < self.terrain.height):
                    p.death_action(self)
                else:
                    self.physicsObjects.add(p)

    def explosion(self, x: int, y: int, radius: int, damage: int, force_coef: float):
        self.terrain.explode_circle(x, y, radius)
        for ent in self.physicsObjects:
            distance = ent.pos.distance_to((x, y)) - math.hypot(ent.radius, ent.radius)
            if distance < radius:
                ent.stable = False
                angle = math.atan2(ent.y - y, ent.x - x)
                ent.vel += Vector2(math.cos(angle), math.sin(angle)) \
                           * force_coef * radius * ((radius - distance) / radius)

                if isinstance(ent, Worm):
                    ent.health -= damage
                    ent.draw_health()

        for _ in range(radius // 2):
            if self.debrisCount == MAX_DEBRIS_COUNT:
                break
            angle = random.random() * math.pi * 2
            debris = Debris(x, y)
            debris.vel_x = math.cos(angle) * radius * 1.5
            debris.vel_y = math.sin(angle) * radius * 1.5
            self.physicsObjects.add(debris)
            self.debrisCount += 1

    def draw(self):
        Renderer2D.submit((self.backgroundImage, (0, 0)))
        Renderer2D.submit((self.terrain.terrainImage, (0, 0)))
        for obj in self.physicsObjects:
            obj.draw()

    @property
    def sel_worm(self):
        return self.teamManager.sel_team.sel_worm
