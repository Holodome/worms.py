import json

import pygame

from .world import World


class WorldLoader:
    @staticmethod
    def load_world_from_json(filepath: str) -> World:
        with open(filepath) as file:
            world_data: dict = json.load(file)

            name = world_data["name"]

            width = world_data["width"]
            height = world_data["height"]

            background_image = None
            background_path = world_data.get("background")
            if background_path is not None:
                background_image = pygame.transform.smoothscale(pygame.image.load(background_path).convert(),
                                                                (width, height))

            foreground_image = None
            foreground_path = world_data.get("foreground")
            if foreground_path is not None:
                foreground_image = pygame.transform.smoothscale(pygame.image.load(foreground_path).convert_alpha(),
                                                                (width, height))

            return World(name, width, height,
                         background_image, foreground_image)

    @staticmethod
    def load_world_save_from_csv(filepath: str) -> None:
        return None
