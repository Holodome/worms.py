from .physicsObject import *
import os


class Worm(PhysicsObject):
    image = pygame.image.load(os.path.join("res/images/worm.png"))
    image.set_colorkey(PhysicsObject.COLORKEY)
    image.convert()

    flipped_image = pygame.transform.flip(image, True, False)

    def __init__(self, name: str, team_color: tuple, x: float, y: float):
        super().__init__(x, y, 7, 0.4)
        self.name: pygame.Surface = self.font.render(name, False, team_color)
        self.color: tuple = team_color

        self.health: int = 100
        self.healthImage: pygame.Surface = self.font.render(str(self.health), False, self.color)
        self.direction = True

    def draw(self, screen: pygame.Surface, offset):
        draw_position = self.position - (6, 7) + offset
        screen.blit(self.image if self.direction else self.flipped_image, draw_position)
        screen.blit(self.name, draw_position + (-self.name.get_width() // 2 + self.image.get_width() // 2, -20))
        screen.blit(self.healthImage, draw_position + (0, -10))

    def redraw_health(self):
        self.healthImage = self.font.render(str(self.health), False, self.color)

