from typing import Tuple

import pygame

from engine.loader import Loader
from .physicsObject import PhysicsCircleObject

name_font = Loader.get_font("consolas", 10)
# Изображение червяка динамическое и завсит от направления последнего движения
image = Loader.load_image("worm")
flipped_image = pygame.transform.flip(image, True, False)


class Worm(PhysicsCircleObject):
    IMAGE = image

    def __init__(self, name: str, team_color):
        PhysicsCircleObject.__init__(self, 0, 0, 7, 0.4)
        self.name: str = name
        self.name_image = name_font.render(name, False, team_color)

        self.color: Tuple[int, int, int] = team_color

        self.health: int = 100
        self.draw_health()

        self.headedRight: bool = True

    def draw_health(self) -> None:
        self.healthImage = name_font.render(str(self.health), False, self.color)

    def is_valid(self):
        return PhysicsCircleObject.is_valid(self) and self.health > 0
