import colorsys
import random
from typing import *

from .gameObjects.worm import Worm
from .weapons import Weapons


class Team:
    with open("data/wormNames.txt") as f:
        Names: List[str] = f.read().split("\n")

    def __init__(self, color: Tuple[int, int, int], worms_number: int):
        self.color: Tuple[int, int, int] = color

        self.wormList: List[Worm] = []
        for _ in range(worms_number):
            self.wormList.append(Worm(self._get_name(), self.color))

        self.selectedWormIndex: int = 0

        self.selectedWeaponId: int = 3
        self.weaponTimeToExplode: int = 3

    def set_worm_random_positions(self, world_width: int) -> None:
        for worm in self.wormList:
            worm.x = random.randrange(world_width // 10, world_width * 9 // 10)
            worm.y = 0

    def set_worm_positions(self, worms_positions: List[Tuple[int, int]]) -> None:
        assert len(self.wormList) == len(worms_positions), "Incorrect positions count"
        for worm, (x, y) in zip(self.wormList, worms_positions):
            worm.x = x
            worm.y = y

    def select_next(self) -> Worm:
        self.selectedWormIndex = (self.selectedWormIndex + 1) % self.get_worms_alive_count()
        return self.wormList[self.selectedWormIndex]

    def select_previous(self) -> Worm:
        if self.selectedWormIndex == 0:
            self.selectedWormIndex = self.get_worms_alive_count() - 1
        else:
            self.selectedWormIndex -= 1
        return self.wormList[self.selectedWormIndex]

    def _get_name(self) -> str:
        return random.choice(Team.Names)

    def get_worms_alive_count(self) -> int:
        return len(self.wormList)

    @property
    def sel_worm(self):
        return self.wormList[self.selectedWormIndex]

    def get_weapon(self):
        return Weapons[self.selectedWeaponId]


class TeamManager:
    def __init__(self, team_data: List[int] = None):
        self.teams: List[Team] = []

        self.selectedTeamIndex = 0
        if team_data is None:
            self.numberOfTeams = 2
            for i in range(2):
                team = Team(((i == 0) * 255, 0, (i != 0) * 255), 5)
                self.teams.append(team)
        else:
            self.numberOfTeams = len(team_data)
            for i, n_worms in enumerate(team_data):
                angle = i / self.numberOfTeams
                team = Team(tuple(map(lambda n: n * 255, colorsys.hsv_to_rgb(angle, 1, 1))), n_worms)
                self.teams.append(team)

    def set_team_positions(self, positions: List[List[Tuple[int, int]]] = None, world_width: int = None):
        assert positions is not None or world_width is not None
        if positions is not None:
            for i, team in enumerate(self.teams):
                team.set_worm_positions(positions[i])
        else:
            for team in self.teams:
                team.set_worm_random_positions(world_width)

    @property
    def sel_team(self):
        return self.teams[self.selectedTeamIndex]
