import json
import os

import pygame

from world.world import World


def load_from_json(path: str) -> World:
    with open(os.path.join(path)) as file:
        world_data: dict = json.load(file)

        name = world_data["name"]

        width = world_data["width"]
        height = world_data["height"]

        teams = world_data.get("teams")

        background = world_data.get("background")
        if background is not None:
            background = pygame.transform.scale(pygame.image.load(os.path.join(background)).convert(),
                                                (width, height))

        foreground = world_data.get("foreground")
        if foreground is not None:
            foreground = pygame.transform.scale(pygame.image.load(os.path.join(foreground)).convert_alpha(),
                                                (width, height))

        wind = world_data.get("windSpeed", 0)
        explosions = world_data.get("allowExplosions", True)

        return World(name,
                     width, height,
                     team_data=teams,
                     background=background, foreground=foreground,
                     wind_speed=wind, allow_explosions=explosions)
