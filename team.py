import os
import random

from gameObjects import Worm


class Team:
    # Get worm names
    with open(os.path.join("res/data/wormNames.txt")) as f:
        names = f.read().split("\n")

    def __init__(self, world_width, color: tuple, worms_number: int, worms_positions: tuple = None):
        self.color = color
        # Team color - with which names will be drawn

        self.worms_number = 0  # Maximum number of worms in team
        self.worms = []
        # Worms info

        for i in range(worms_number):
            x = random.randrange(world_width - Worm.image.get_width())
            y = 0
            if worms_positions is not None:
                x, y = worms_positions[i]
            self.worms.append(Worm(self._get_name(), color, x, y))
            self.worms_number += 1

        self.selectedWormIndex = 0
        # Index of selected worm
        self.selected_weapon: None = None
        # TODO implement weapons

    def select_next(self):
        self.selectedWormIndex = (self.selectedWormIndex + 1) % self.worms_alive

    def select_previous(self):
        if self.selected_worm == 0:
            self.selectedWormIndex = self.worms_alive
        else:
            self.selectedWormIndex -= 1

    def _get_name(self) -> str:
        """
        Returns name for a worm
        First tries to find not used name
        If all names are used returns random
        """
        excluded_names = tuple(filter(lambda worm: worm.name, self.worms))
        possible_names = self.names
        if self.worms_number < len(self.names):
            possible_names = tuple(filter(lambda name: name not in excluded_names, possible_names))

        return random.choice(possible_names)

    @property
    def worms_alive(self):
        return len(self.worms)

    @property
    def selected_worm(self):
        return self.worms[self.selectedWormIndex]
