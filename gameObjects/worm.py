import pygame
from .physicsObject import PhysicsObject
import os


class Worm(PhysicsObject):
    image = pygame.image.load(os.path.join("res/images/worm.png"))
    image.set_colorkey(PhysicsObject.COLORKEY)
    image.convert()

    font = pygame.font.SysFont("consolas", 10)

    def __init__(self, name: str, team_color: tuple, x: float, y: float):
        super().__init__(x, y, 7, 0.4, -1)
        self.name: pygame.Surface = self.font.render(name, False, team_color)
        self.color: tuple = team_color

        self.health: int = 100
        self.healthImage: pygame.Surface = self.font.render(str(self.health), False, self.color)

    def draw(self, screen: pygame.Surface, offset):
        draw_position = self.position - (6, 7) + offset
        screen.blit(self.image, draw_position)
        screen.blit(self.name, draw_position + (-self.name.get_width() / 4, -20))
        screen.blit(self.healthImage, draw_position + (0, -10))

    def redraw_health(self):
        self.healthImage: pygame.Surface = self.font.render(str(self.health), False, self.color)

    @property
    def alive(self):
        return self.health > 0
