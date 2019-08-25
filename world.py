import numpy
import pygame

import os
import json

from team import Team
import colorsys  # hsv_to_rgb

ALPHA_COLORKEY = (255, 0, 255)
CAMERA_SPEED = 1000
GRAVITY = 500


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
        self.cameraPosition = numpy.zeros(2, dtype=numpy.uint16)  # Left-top corner
        self.cameraStickToPlayer: bool = True

    def update(self):
        """
        Update camera
        """
        if self.cameraStickToPlayer:
            self._apply_camera(self.world.selected_team.selected_worm)

    def draw(self, screen: pygame.Surface):
        """
        Draws world - main purpose of this class
        """
        # (-self.cameraPosition[0], -self.cameraPosition[1]) is an offset for simulating camera
        if self.world.backgroundImage is not None:
            screen.blit(self.world.backgroundImage, (-self.cameraPosition[0], -self.cameraPosition[1]))

        screen.blit(self.world.terrainImage, (-self.cameraPosition[0], -self.cameraPosition[1]))
        for entity in self.world.entities:
            entity.draw(screen)

    def move_camera(self, dt: float, x: int, y: int):
        self.cameraStickToPlayer = False  # If camera moved manually - disable following (toggle again with R)
        screen_size = pygame.display.get_window_size()  # TODO CHANGE THE WAY OF GETTING SCREEN SIZE FOR SCALED ASAP
        if x != 0:
            self.cameraPosition[0] = min(  # Use round() instead of floor to achieve same movement in both directions
                max(round(self.cameraPosition[0] + x * dt * CAMERA_SPEED), 0),
                self.world.worldSize[0] - screen_size[0])
        if y != 0:
            self.cameraPosition[1] = min(
                max(round(self.cameraPosition[1] + y * dt * CAMERA_SPEED), 0),
                self.world.worldSize[1] - screen_size[1])

    def _apply_camera(self, entity):
        screen_size = pygame.display.get_window_size()  # TODO CHANGE THE WAY OF GETTING SCREEN SIZE FOR SCALED ASAP
        self.cameraPosition[0] = min(
            max(round(entity.x - screen_size[0]), 0),
            self.world.worldSize[0] - screen_size[0])
        self.cameraPosition[1] = min(
            max(round(entity.y - screen_size[1]), 0),
            self.world.worldSize[1] - screen_size[1])


class World:
    """
    Class representing the single world (or level) in game
    """

    def __init__(self, name: str,
                 width: int, height: int,
                 team_data: list = None,
                 background: pygame.Surface = None, foreground: pygame.Surface = None,
                 wind_speed: float = 0, allow_explosions: bool = False):
        # World name
        self.name: str = name
        # Terrain is represented by one-dimensional array of integers
        # Each of which represents the state on the block with corresponding coordinate
        self.terrain: numpy.array = numpy.zeros(width * height, numpy.uint8)
        self.worldSize: tuple = (width, height)
        # All entities are located in one list
        self.entities: list = []
        # Teams contain certain amount of worms
        # Which players have access to
        self.wormsTeams: list = []
        self.wormsTeamIndex = 0
        # If team data is not specified make 2 teams with 5 worms
        if team_data is None:
            for i in range(2):
                team = Team((i == 0, 0, i != 0), 5)  # 1 team is red, 2 is blue
                self.wormsTeams.append(team)
                self.entities.extend(team.worms)
        else:
            n_teams = len(team_data)
            for i, n_worms in enumerate(team_data):
                angle = i * n_teams / 360  # Not to hard-code colors use hsv values
                team = Team(colorsys.hsv_to_rgb(angle, 1, 1), n_worms)
                self.wormsTeams.append(team)
                self.entities.extend(team.worms)

        # Wind speed affect all game objects
        self.windSpeed: float = wind_speed
        # Can explosions damage terrain
        self.allowExplosions: bool = allow_explosions

        if background is not None:
            self.backgroundImage = background.convert()
        else:
            self.backgroundImage = None

        if foreground is not None:
            self._load_foreground_as_terrain(foreground)
        else:
            self._generate_random_terrain()

        # Terrain image is how terrain is represented on the screen
        self.terrainImage = pygame.Surface((width, height))
        self.terrainImage.set_colorkey(ALPHA_COLORKEY)
        self._draw_terrain(0, 0, width, height)

    def update(self, dt: float):
        """
        Update game logic here (physics etc.)
        """
        pass

    def _load_foreground_as_terrain(self, image: pygame.Surface):
        image: pygame.Surface = pygame.transform.scale(image, self.worldSize)
        for x in range(self.worldSize[0]):
            for y in range(self.worldSize[1]):
                # TODO implement using different surface types
                if image.get_at((x, y))[3] != 0:
                    self.terrain[x + y * self.worldSize[0]] = 1

    def _generate_random_terrain(self):
        pass

    def _draw_terrain(self, sx: int, sy: int, width: int, height: int):
        for x in range(sx, sx + width):
            for y in range(sy, sy + height):
                if not 0 <= x < self.worldSize[0] or not 0 <= y < self.worldSize[1]:
                    continue

                color = (255, 0, 255)
                if self.terrain[x + y * self.worldSize[0]] == 1:
                    color = (0, 255, 0)
                self.terrainImage.set_at((x, y), color)

    @property
    def selected_team(self):
        return self.wormsTeams[self.wormsTeamIndex]


def load_from_json(path: str) -> World:
    """
    load_data_from_json -> None
    loads level data from .json file
    :param path: path to .json file
    :return: World as specified
    """
    with open(os.path.join(path), "r") as file:
        world_data: dict = json.load(file)

        name = world_data["name"]

        width = world_data["width"]  # Width and height represent actual world size
        height = world_data["height"]

        teams = world_data.get("teams")

        background = world_data.get("background")
        if background is not None:
            background = pygame.transform.scale(pygame.image.load(os.path.join(background)).convert(),
                                                (width, height))  # Resize Image to fit the world
        foreground = world_data.get("foreground")
        if foreground is not None:
            # TODO use colorkey instead of alpha
            foreground = pygame.transform.scale(pygame.image.load(os.path.join(foreground)).convert_alpha(),
                                                (width, height))

        wind = world_data.get("windSpeed", 0)
        explosions = world_data.get("allowExplosions", False)

        return World(name,
                     width, height,
                     team_data=teams,
                     background=background, foreground=foreground,
                     wind_speed=wind, allow_explosions=explosions)


def save_as_csv(world):
    pass


if __name__ == "__main__":
    w = load_from_json("")
