import random

from project.gameObjects import Worm
import os


class Team:
    # Get worm names
    with open(os.path.join("res/data/wormNames.txt"), "r") as f:
        names = f.read().split("\n")

    def __init__(self, color: tuple, worms_number: int, worms_positions: tuple = None):
        self.color = color
        # Team color - with which names will be drawn

        self.worms_number = 0  # Maximum number of worms in team
        self.worms = []
        # Worms info

        for i in range(worms_number):
            x = y = 0
            if worms_positions is not None:
                x, y = worms_positions[i]
            self.worms.append(Worm(self._get_name(), color, x, y))
            self.worms_number += 1

        self.selectedWorm = 0
        # Index of selected worm
        self.selected_weapon: None = None
        # TODO implement weapons

    def select_next(self):
        self.selectedWorm = (self.selectedWorm + 1) % self.worms_number

    def _get_name(self) -> str:
        """
        Returns name for a worm
        First tries to find not used name
        If all names are used returns random
        :return: Worm name
        """
        excluded_names = tuple(filter(lambda worm: worm.name, self.worms))
        possible_names = self.names
        if self.worms_number < len(self.names):
            possible_names = tuple(filter(lambda name: name not in excluded_names, possible_names))

        return random.choice(possible_names)

    @property
    def worms_alive(self):
        return sum(map(lambda worm: worm.alive, self.worms))

    @property
    def selected_worm(self):
        return self.worms[self.selectedWorm]
