import numpy
import pygame

import os
import json
import math
from team import Team
import colorsys  # hsv_to_rgb

ALPHA_COLORKEY = (255, 0, 255)
CAMERA_SPEED = 1000
GRAVITY = 1000


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
        offset = (-self.cameraPosition[0], -self.cameraPosition[1])
        if self.world.backgroundImage is not None:
            screen.blit(self.world.backgroundImage, offset)

        screen.blit(self.world.terrainImage, offset)

        for entity in self.world.entities:
            entity.draw(screen, offset)

    def move_camera(self, dt: float, x: int, y: int):
        self.cameraStickToPlayer = False  # If camera moved manually - disable following (toggle again with R)
        if x != 0:
            self.cameraPosition[0] = min(  # Use round() instead of floor to achieve same movement in both directions
                max(round(self.cameraPosition[0] + x * dt * CAMERA_SPEED), 0),
                self.world.worldSize[0] - self.screenSize[0])
        if y != 0:
            self.cameraPosition[1] = min(
                max(round(self.cameraPosition[1] + y * dt * CAMERA_SPEED), 0),
                self.world.worldSize[1] - self.screenSize[1])

    def _apply_camera(self, entity):
        self.cameraPosition[0] = min(
            max(round(entity.x - self.screenSize[0] / 2), 0),
            self.world.worldSize[0] - self.screenSize[0])
        self.cameraPosition[1] = min(
            max(round(entity.y - self.screenSize[1] / 2), 0),
            self.world.worldSize[1] - self.screenSize[1])


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
        self.terrain: numpy.array = numpy.zeros(width * height, numpy.uint32)
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
                team = Team(self.worldSize[0], (i == 0, 0, i != 0), 5)  # 1 team is red, 2 is blue
                self.wormsTeams.append(team)
                self.entities.extend(team.worms)
        else:
            n_teams = len(team_data)
            for i, n_worms in enumerate(team_data):
                angle = i / n_teams  # using hsv allows to pick colors using simple fraction
                team = Team(self.worldSize[0], tuple(map(lambda n: n * 255, colorsys.hsv_to_rgb(angle, 1, 1))), n_worms)
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
        for _ in range(6):  # Update times - better precision
            for entity in self.entities:
                entity.acceleration.y += GRAVITY * dt
                entity.velocity += entity.acceleration * dt
                potential_position = entity.position + entity.velocity * dt
                # Reset acceleration
                entity.acceleration = pygame.Vector2(0, 0)
                entity.stable = False
                # Calculate response force
                angle = entity.angle
                response = pygame.Vector2(0, 0)
                collided = False
                # Iterate through angles on semicircle with center point in angle
                for r in map(lambda n: (n / 8.0) * math.pi + (angle - math.pi / 2.0), range(8)):
                    test_position = pygame.Vector2(entity.radius * math.cos(r), entity.radius * math.sin(r)) \
                                    + potential_position
                    if not (0 <= test_position.x < self.worldSize[0]) or not \
                            (0 <= test_position.y < self.worldSize[1]):
                        continue

                    if self.terrain[int(test_position.x) + int(test_position.y) * self.worldSize[0]] != 0:
                        response += potential_position - test_position
                        collided = True

                if collided:
                    response_magnitude = response.magnitude()

                    entity.stable = True
                    reflection = entity.velocity.x * (response.x / response_magnitude) + \
                                 entity.velocity.y * (response.y / response_magnitude)
                    entity.velocity = (entity.velocity + (response / response_magnitude * -2.0 * reflection)) \
                                      * entity.friction

                else:
                    if 0 <= potential_position.x < self.worldSize[0]:  # If x position is correct
                        entity.position = potential_position
                    else:
                        # Add some speed to go in the opposite way
                        entity.velocity.x += 20 * (1 if potential_position.x < 0 else -1)

    def _load_foreground_as_terrain(self, image: pygame.Surface):
        for x in range(self.worldSize[0]):
            for y in range(self.worldSize[1]):
                pix = image.get_at((x, y))
                if pix[3] != 0:  # Not transparent
                    # Store color data in one integer using bitwise operators
                    data = ((pix[0] << 16) & 0xFF0000) | ((pix[1] << 8) & 0x00FF00) | pix[2] & 0x0000FF
                    self.terrain[x + y * self.worldSize[0]] = data

    def _generate_random_terrain(self):
        pass

    def _draw_terrain(self, sx: int, sy: int, width: int, height: int):
        for x in range(sx, sx + width):
            for y in range(sy, sy + height):
                if not 0 <= x < self.worldSize[0] or not 0 <= y < self.worldSize[1]:
                    continue
                color = (255, 0, 255)
                cell = self.terrain[x + y * self.worldSize[0]]
                if cell != 0:
                    color = ((cell >> 16) & 0xFF, (cell >> 8) & 0xFF, cell & 0xFF)
                self.terrainImage.set_at((x, y), color)

    @property
    def selected_team(self) -> Team:
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


def load_from_csv(path):
    return None


if __name__ == "__main__":
    w = load_from_json("")
