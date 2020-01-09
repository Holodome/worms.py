import math
import random
from typing import *

import pygame

from engine import Renderer, Vector2
from .gameObjects.particles import Debris
from .gameObjects.physicsObject import PhysicsObject
from .terrain import Terrain
from .wormsTeam import TeamManager

GRAVITY_ACC = 1000
SAMPLE_TIMES = 8


class World:
    def __init__(self, name: str, width: int, height: int,
                 background: pygame.Surface, foreground: pygame.Surface):
        self.name: str = name
        self.terrain: Terrain = Terrain(width, height, foreground)

        self.physicsObjects: List[PhysicsObject] = []

        self.backgroundImage: pygame.Surface = background

        self.teamManager: TeamManager = TeamManager()
        self.teamManager.set_team_positions(world_width=width)
        for team in self.teamManager.teams:
            for worm in team.wormList:
                self.physicsObjects.append(worm)

    def on_update(self, timestep):
        for _ in range(4):
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
                response = Vector2(0, 0)
                collided = False
                for r in map(lambda n: (n / SAMPLE_TIMES) * math.pi + (ent.angle - math.pi / 2.0), range(SAMPLE_TIMES)):
                    test_pos = Vector2(ent.radius * math.cos(r), ent.radius * math.sin(r)) + potential_pos
                    if self.terrain.valid_position(int(test_pos.x), int(test_pos.y)) \
                            and self.terrain.get_block_data(int(test_pos.x), int(test_pos.y)):
                        response += potential_pos - test_pos
                        collided = True
                if not collided and ent.is_bullet():
                    collided = ent.check_collisions(self.physicsObjects)
                    if collided:
                        response = potential_pos - ent.pos
                # Результат проверки столкновений
                if collided:  # Если объект столкунлся с землей - направить скорость в обратную сторону
                    ent.set_response(response)
                else:  # Если столкновения не произошло - продолжить движение
                    ent.pos = potential_pos

                if not ent.is_valid():
                    ent.Alive = False
                else:
                    ent.finish_update()

            old = self.physicsObjects.copy()
            self.physicsObjects.clear()
            for p in old:
                p.Alive = (0 <= p.x < self.terrain.width and 0 <= p.y < self.terrain.height) if p.Alive else False
                if not p.Alive:
                    p.death_action(self)
                else:
                    self.physicsObjects.append(p)

    def explosion(self, x: int, y: int, radius: int, damage: int, force_coef: float):
        self.terrain.explode_circle(x, y, radius)
        for ent in self.physicsObjects:
            distance = ent.pos.distance_to((x, y)) - math.hypot(ent.radius, ent.radius)
            if distance < radius:
                ent.stable = False
                angle = math.atan2(ent.y - y, ent.x - x)
                ent.vel += Vector2(math.cos(angle), math.sin(angle)) \
                           * force_coef * radius * ((radius - distance) / radius)

                if ent.is_worm():
                    ent.health -= damage
                    ent.draw_health()

        for _ in range(radius // 2):
            angle = random.random() * math.pi * 2
            debris = Debris(x, y)
            debris.vel_x = math.cos(angle) * radius * 1.5
            debris.vel_y = math.sin(angle) * radius * 1.5
            self.physicsObjects.append(debris)

    def draw(self):
        Renderer.submit((self.backgroundImage, (0, 0)))
        Renderer.submit((self.terrain.terrainImage, (0, 0)))
        for obj in self.physicsObjects:
            obj.draw()

    @property
    def sel_worm(self):
        return self.teamManager.sel_team.sel_worm
