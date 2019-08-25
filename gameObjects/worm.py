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
        self.name: str = name
        self.color: tuple = team_color

        self.health: int = 100

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.position)
        screen.blit(self.font.render(self.name, False, self.color), self.position + (0, -20))
        screen.blit(self.font.render(str(self.health), False, self.color), self.position + (0, -10))

    @property
    def alive(self):
        return self.health > 0