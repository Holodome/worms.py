import pygame

import sys
import enum

from project.world import load_from_json


# Game states
class State(enum.Enum):
    GAME_ACTIVE = 1
    GAME_PAUSED = 2
    GAME_MENU = 3


class Worms:
    """
    Game class
    """

    def __init__(self):

        self.state: State = State.GAME_ACTIVE

        self.world = load_from_json("res/levels/test.json")  # TEST VARIANT - TODO make loading in menu

        # Fonts
        self.debugFont = pygame.font.SysFont("Consolas", 15)
        self.menuFont = pygame.font.SysFont("comicsans", 50)

        self.showDebugInfo: bool = True
        self.FPS: float = 0

    def event(self, dt: float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F3:
                    self.showDebugInfo = not self.showDebugInfo

                elif event.key == pygame.K_r:  # Reset camera sticking to player
                    self.world.cameraStickToPlayer = True

        pressed = pygame.key.get_pressed()
        # Move camera
        if pressed[pygame.K_w]:
            self.world.move_camera(dt, 0, -1)
        elif pressed[pygame.K_s]:
            self.world.move_camera(dt, 0, 1)
        elif pressed[pygame.K_a]:
            self.world.move_camera(dt, -1, 0)
        elif pressed[pygame.K_d]:
            self.world.move_camera(dt, 1, 0)

    def update(self, dt: float):
        # Update time

        # Save data for debug screen
        if self.showDebugInfo:
            self.FPS = 1 / dt

        self.world.update(dt)

    def draw(self, screen: pygame.Surface):
        if self.state == State.GAME_ACTIVE:
            self.world.draw(screen)

        elif self.state == State.GAME_MENU:
            # TODO add play button to menu
            menu = self.menuFont.render("Menu", False, (255, 0, 0))
            screen.blit(menu, ((screen.get_width() - menu.get_width()) / 2, screen.get_height() / 4))

        if self.showDebugInfo:
            screen.blit(self.debugFont.render(f"FPS: {'{0:.2f}'.format(self.FPS)}", False, (255, 0, 0)), (0, 0))
            screen.blit(
                self.debugFont.render(f"Camera stick to player: {self.world.cameraStickToPlayer}", False, (255, 0, 0)),
                (0, 15))
            screen.blit(self.debugFont.render(f"Camera Position: {self.world.cameraPosition}", False, (255, 0, 0)),
                        (0, 30))
