import math
import random

import pygame

from gameObjects import *
from world.teams.team_manager import TeamManager
from world.terrain import Terrain

GRAVITY = 1000


class World:
    def __init__(self, name: str,
                 width: int, height: int,
                 team_data: list = None,
                 background: pygame.Surface = None, foreground: pygame.Surface = None,
                 wind_speed: float = 0, allow_explosions: bool = False):
        self.name: str = name
        self.terrain: Terrain = Terrain(width, height, foreground)

        self.entities: list = []
        self.team_manager: TeamManager = TeamManager(width, team_data, self.entities)

        self.windSpeed: float = wind_speed
        # Can explosions damage terrain
        self.allowExplosions: bool = allow_explosions
        self.debrisAllowed: bool = True

        self.backgroundImage = background

    def update(self, dt: float):
        update_times = 6
        for _ in range(update_times):
            entities = self.entities.copy()
            self.entities.clear()
            for entity in entities:
                if entity.timeToDeath != -1:
                    entity.timeToDeath -= dt / update_times
                    if entity.timeToDeath <= 0:
                        entity.death_action(self)
                        continue

                if entity.affectedByGravity:
                    acceleration = GRAVITY * dt
                    entity.velocity.y += acceleration * dt
                potential_position = entity.position + entity.velocity * dt
                entity.stable = False

                response = pygame.Vector2(0, 0)
                collided = False
                # CIRCLE - TERRAIN COLLISION
                for r in map(lambda n: (n / 8.0) * math.pi + (entity.angle - math.pi / 2.0), range(8)):
                    test_position = pygame.Vector2(entity.radius * math.cos(r), entity.radius * math.sin(r)) \
                                    + potential_position
                    if self.terrain.valid_position(*test_position) and self.terrain.get_block_data(*test_position) != 0:
                        response += potential_position - test_position
                        collided = True

                if collided:
                    response_magnitude = response.magnitude()
                    entity.stable = True
                    reflection = entity.velocity.x * (response.x / response_magnitude) + \
                                 entity.velocity.y * (response.y / response_magnitude)
                    entity.velocity = (entity.velocity + (response / response_magnitude * -2.0 * reflection)) \
                                      * entity.friction
                    if entity.bounceTimes > 0:
                        entity.bounceTimes -= 1
                        if entity.bounceTimes == 0:
                            entity.death_action(self)
                else:
                    entity.position = potential_position

                if entity.valid(self.terrain.size):
                    if abs(entity.velocity.magnitude()) < 0.001:  # Delete small movement
                        entity.stable = True
                        entity.velocity -= entity.velocity
                    if isinstance(entity, Worm) and entity.velocity != 0 and not entity.stable:
                        entity.direction = entity.velocity.x > 0
                    self.entities.append(entity)
                elif isinstance(entity, Worm):
                    self.team_manager.remove_worm(entity)

    def explosion(self, x: int, y: int, radius: int, damage: int, force_coefficient: float):
        if self.allowExplosions:
            self.terrain.explode_circle(x, y, radius)
        for entity in self.entities:  # Apply forces to other entities
            distance = entity.position.distance_to((x, y)) - entity.center_dist
            if distance < radius:
                entity.stable = False
                angle = math.atan2(entity.y - y, entity.x - x)
                entity.velocity += pygame.Vector2(math.cos(angle), math.sin(angle)) * force_coefficient * radius \
                                   * ((radius - distance) / radius)
                if isinstance(entity, Worm):
                    entity.health -= damage
                    entity.redraw_health()

        if self.debrisAllowed:
            for _ in range(radius // 2):
                angle = random.random() * math.pi * 2
                self.entities.append(Debris(x, y, math.cos(angle) * radius * 1.5, math.sin(angle) * radius * 1.5))
