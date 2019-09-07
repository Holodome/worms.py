import os
import random

import loader
from gameObjects import *
from weapon_manager import WeaponManager

worm_image_width = loader.get_image("worm").get_width()


class Team:
    # Get worm names
    with open(os.path.join("res/data/wormNames.txt")) as f:
        names = f.read().split("\n")

    def __init__(self, world_width, color: tuple, worms_number: int, worms_positions: tuple = None):
        self.color = color
        # Team color - with which names will be drawn

        self.worms = []
        # Worms info

        for i in range(worms_number):
            x = random.randrange(world_width - worm_image_width)
            y = 0
            if worms_positions is not None:
                x, y = worms_positions[i]
            self.worms.append(Worm(self._get_name(worms_number), color, x, y))

        self.selectedWormIndex = 0
        self.weapon_manager: WeaponManager = WeaponManager()

    def select_next(self):
        self.selectedWormIndex = (self.selectedWormIndex + 1) % self.worms_alive
        return self.worms[self.selectedWormIndex]

    def select_previous(self):
        if self.selected_worm == 0:
            self.selectedWormIndex = self.worms_alive - 1
        else:
            self.selectedWormIndex -= 1
        return self.worms[self.selectedWormIndex]

    def _get_name(self, worms_number) -> str:
        """
        Returns name for a worm
        First tries to find not used name
        If all names are used returns random
        """
        excluded_names = tuple(filter(lambda worm: worm.name, self.worms))
        possible_names = self.names
        if worms_number < len(self.names):
            possible_names = tuple(filter(lambda name: name not in excluded_names, possible_names))

        return random.choice(possible_names)

    @property
    def worms_alive(self):
        return len(self.worms)

    @property
    def selected_worm(self):
        return self.worms[self.selectedWormIndex]
