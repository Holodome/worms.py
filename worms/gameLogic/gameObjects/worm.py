from typing import Tuple

import pygame

from engine.loader import Loader
from engine.renderer.entity import Entity
from engine.renderer.renderer2D import Renderer2D
from .physicsObject import PhysicsCircleObject


class Worm(PhysicsCircleObject):
    name_font = Loader.get_font("BerlinSans.TTF", 10)
    # Изображение червяка динамическое и завсит от направления последнего движения
    image = Loader.load_image("worm")
    image.set_colorkey((255, 0, 255))
    flipped_image = pygame.transform.flip(image, True, False)

    IMAGE_OFFSET = image.get_width() / 2, image.get_height() / 2

    IMAGE = image

    def __init__(self, name: str, team_color):
        PhysicsCircleObject.__init__(self, 0, 0, 7, 0.4)
        self.name: str = name
        self.nameImage: pygame.Surface = Worm.name_font.render(name, False, team_color)

        self.nameImageOffset = (-self.nameImage.get_width() // 2 + self.image.get_width() // 2, -20)

        self.color: Tuple[int, int, int] = team_color

        self.health: int = 100
        self.draw_health()

        self.headedRight: bool = True

    def draw_health(self) -> None:
        self.healthImage = Worm.name_font.render(str(self.health), False, self.color)

    def is_valid(self) -> bool:
        return PhysicsCircleObject.is_valid(self) and self.health > 0

    @Entity.pos.getter
    def pos(self):
        return self._pos - Worm.IMAGE_OFFSET

    def draw(self):
        if self.headedRight:
            Renderer2D.submit((self.image, self.pos))
        else:
            Renderer2D.submit((self.flipped_image, self.pos))
        Renderer2D.submit((self.nameImage, self.pos + self.nameImageOffset))
        Renderer2D.submit((self.healthImage, self.pos + (0, -10)))
