import colorsys

from world.teams.team import Team
from world.teams.weapon_manager import WeaponManager


class TeamManager:
    def __init__(self, width, team_data, entities):
        self.teams: list = []
        self.weapon_managers = []

        self.selected_team_ind = 0
        self.number_of_teams = 2
        if team_data is None:
            for i in range(2):
                team = Team(width, (i == 0, 0, i != 0), 5)
                self.teams.append(team)
                entities.extend(team.worms)
        else:
            self.number_of_teams = len(team_data)
            for i, n_worms in enumerate(team_data):
                angle = i / self.number_of_teams  # using hsv allows to pick colors using simple fraction
                team = Team(width, tuple(map(lambda n: n * 255, colorsys.hsv_to_rgb(angle, 1, 1))), n_worms)
                self.teams.append(team)
                entities.extend(team.worms)

        for _ in range(self.number_of_teams):
            self.weapon_managers.append(WeaponManager())

    def remove_worm(self, worm):
        for team in self.teams:
            if worm in team.worms:
                team.worms.remove(worm)
                team.select_next()
                break

    @property
    def selected_team(self) -> Team:
        return self.teams[self.selected_team_ind]

    @property
    def selected_weapon_manager(self) -> WeaponManager:
        return self.weapon_managers[self.selected_team_ind]
