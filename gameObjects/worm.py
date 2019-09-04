import loader
from .physicsObject import *

font = loader.get_font("consolas", 10)
image = loader.get_image("worm")
flipped_image = pygame.transform.flip(image, True, False)


class Worm(PhysicsObject):
    center_dist = math.hypot(6, 7)

    def __init__(self, name: str, team_color: tuple, x: float, y: float):
        super().__init__(x, y, 7, 0.4)
        self.name: pygame.Surface = font.render(name, False, team_color)
        self.color: tuple = team_color

        self.health: int = 100
        self.healthImage: pygame.Surface = font.render(str(self.health), False, self.color)
        self.direction = True

    def draw(self, screen: pygame.Surface, offset):
        draw_position = self.position - (6, 7) + offset
        screen.blit(image if self.direction else flipped_image, draw_position)
        screen.blit(self.name, draw_position + (-self.name.get_width() // 2 + image.get_width() // 2, -20))
        screen.blit(self.healthImage, draw_position + (0, -10))

    def redraw_health(self):
        self.healthImage = font.render(str(self.health), False, self.color)

    def valid(self, world_size):
        return super().valid(world_size) and self.health > 0
