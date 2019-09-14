import math

import numpy
import pygame

from gameObjects import *
from toolbox import *

arrow_image = get_image("arrow")
crosshair_image = get_image("crosshair")
CAMERA_SPEED = 1000


class Arrow:
    """
    Red arrow jumping above selected worm
    """

    def __init__(self):
        self.position: float = 5
        self.isUp: bool = True

    def update(self, dt):
        self.position = max(min(self.position + (self.isUp or -1) * 10 * dt, 5), 0)
        if self.position == 5 or self.position == 0:
            self.isUp = not self.isUp

    def draw(self, screen, position):
        screen.blit(arrow_image, tuple(map(int, position + (0, int(self.position ** 2) - 25))))


class WorldRenderer:
    """
    Class for separating draw logic from game logic
    It keeps information about camera, and uses world attributes such as images to draw it
     (because images are part of the world and cannot be separated)
    """

    def __init__(self, world, screen_size):
        self.screenSize = screen_size

        self.world = world

        # Camera
        self.cameraPosition = numpy.zeros(2, dtype=numpy.uint16)
        self.cameraStickToPlayer: bool = True

        self.cameraTrackingEntity = self.world.team_manager.selected_team.selected_worm
        # Arrow
        self.arrow = Arrow()

        self.notInAnimation: bool = True
        self.aimState: bool = True

    def update(self, dt):
        if self.cameraStickToPlayer:
            self._apply_camera(self.cameraTrackingEntity)

        if self.notInAnimation:
            self.arrow.update(dt)
        else:
            if not any(map(lambda e: not isinstance(e, Worm), self.world.entities)):
                # Simple check if all existing entities are not worms - possibly add other in whitelist
                self.notInAnimation = True
                self.cameraTrackingEntity = self.world.team_manager.selected_team.selected_worm

    def draw(self, screen: pygame.Surface):
        offset = self.offset
        if self.world.backgroundImage is not None:
            screen.blit(self.world.backgroundImage, offset)

        screen.blit(self.world.terrain.terrainImage, offset)

        for entity in self.world.entities:
            entity.draw(screen, offset)

        if self.notInAnimation:
            self.arrow.draw(screen, self.cameraTrackingEntity.position - (6, 40) + offset)
            if self.aimState:
                screen.blit(crosshair_image,
                            self.cameraTrackingEntity.position + (-5, -5) +
                            self.offset + (
                            math.cos(self.world.team_manager.selected_weapon_manager.shootingAngle) * 40,
                            math.sin(self.world.team_manager.selected_weapon_manager.shootingAngle) * 40))

    def draw_force_bar(self, screen: pygame.Surface, force: float):
        position = self.cameraTrackingEntity.position + (-10, 25) + self.offset
        green_length = int(force * 20)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(*position, green_length, 2))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(*(position + (green_length, 0)), 20 - green_length, 2))

    def move_camera(self, dt: float, x: int, y: int):
        self.cameraStickToPlayer = False  # If camera moved manually - disable following (toggle again with R)
        if x != 0:
            self.cameraPosition[0] = min(  # Use round() instead of floor to achieve same movement in both directions
                max(round(self.cameraPosition[0] + x * dt * CAMERA_SPEED), 0),
                self.world.terrain.width - self.screenSize[0])
        if y != 0:
            self.cameraPosition[1] = min(
                max(round(self.cameraPosition[1] + y * dt * CAMERA_SPEED), 0),
                self.world.terrain.height - self.screenSize[1])

    def set_weapon_fired(self, entity):
        self.notInAnimation = False
        self.cameraTrackingEntity = entity

    def _apply_camera(self, entity):
        self.cameraPosition[0] = min(
            max(round(entity.x - self.screenSize[0] / 2), 0),
            self.world.terrain.width - self.screenSize[0])
        self.cameraPosition[1] = min(
            max(round(entity.y - self.screenSize[1] / 2), 0),
            self.world.terrain.height - self.screenSize[1])

    @property
    def offset(self):
        return -int(self.cameraPosition[0]), -int(self.cameraPosition[1])
