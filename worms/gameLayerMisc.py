import pygame

from engine import *
from interface import *

CROSSHAIR_IMAGE = Loader.get_image("crosshair")

FORCE_BAR_OFFSET = (-9, 20)
JUMPING_ARROW_OFFSET = (5, 40)

WEAPON_FIRE_COEF = 50


class ForceBar:
    def __init__(self):
        self.image = pygame.Surface((20, 2))

    def update_force_image(self, force):
        green_length = int(force * self.image.get_width())
        self.image.fill((0, 255, 0), (0, 0, green_length, self.image.get_height()))
        self.image.fill((255, 0, 0), (green_length, 0, 20 - green_length, self.image.get_height()))

    def draw(self, position):
        Renderer.submit((self.image, position + FORCE_BAR_OFFSET))


class JumpingArrow:
    def __init__(self):
        self.image = Loader.get_image("arrow")

        self.vertPos: float = 5
        self.goingUp: bool = True

    def update(self, dt):
        self.vertPos = clamp(self.vertPos + (self.goingUp or -1) * 10 * dt, 0, 5)
        if self.vertPos == 5 or self.vertPos == 0:
            self.goingUp = not self.goingUp

    def draw(self, position):
        Renderer.submit((self.image, vec_to_itup(position + (0, int(self.vertPos ** 2) - 25) - JUMPING_ARROW_OFFSET)))


class Crosshair(Entity):
    def __init__(self):
        super().__init__(Loader.get_image("crosshair"), Vector2(0))

    def draw(self, pos):
        self.pos = pos
        Renderer.submit(self)


class PauseContainer(Container):
    def __init__(self):
        super().__init__(Rect(0, 0, Window.Instance.width, Window.Instance.height))
        self.set_color(Color(50, 50, 50, 230))
        self.paused_label = Label(Loader.get_font("ALoveOfThunder.ttf", 200)
                                  .render("GAME PAUSED", False, (255, 150, 200, 245)))
        self.paused_label.constraints.add_width_constraint(RelativeMultConstraint(0.7))
        self.paused_label.constraints.add_height_constraint(AspectConstraint())
        self.paused_label.constraints.add_x_constraint(CenterConstraint())
        self.paused_label.constraints.add_y_constraint(RelativeAddConstraint(0.25))
        self.add_element(self.paused_label)
