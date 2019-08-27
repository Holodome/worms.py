import enum
import os
import sys

import pygame

from world import WorldRenderer, load_from_json

DEBUG_COLOR = (50, 50, 50)


# Game states
class State(enum.Enum):
    GAME_ACTIVE = 1
    GAME_PAUSED = 2
    GAME_MENU = 3


class Worms:
    """
    Game class
    """
    levels = os.listdir(os.path.join("res/levels"))
    # Load fonts
    titleFont = pygame.font.Font("res/fonts/title.TTF", 40)
    worldFont = pygame.font.Font("res/fonts/worldName.TTF", 20)
    debugFont = pygame.font.SysFont("Consolas", 15)
    menuFont = pygame.font.SysFont("comicsans", 50)

    title = titleFont.render("WORMS.PY", False, (30, 30, 30))

    def __init__(self, screen_size):

        self.state: State = State.GAME_ACTIVE

        self.world = load_from_json("res/levels/bikini_bottom.json")  # TODO make loading in menu
        self.renderer = WorldRenderer(self.world, screen_size)

        self.world_name = self.worldFont.render(self.world.name, False, (100, 100, 100))

        self.showDebugInfo: bool = False
        self.FPS: float = 0

        self.showTitleInGame = True
        self.fullscreen = False

    def event(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.world.debrisAllowed = not self.world.debrisAllowed
                elif event.key == pygame.K_F3:  # Show debug screen
                    self.showDebugInfo = not self.showDebugInfo
                elif event.key == pygame.K_F4:  # Show nice title
                    self.showTitleInGame = not self.showTitleInGame
                elif event.key == pygame.K_F11:  # Toggle fullscreen
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        pygame.display.set_mode(flags=pygame.HWSURFACE | pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode()

                elif event.key == pygame.K_r:  # Reset camera sticking to player
                    self.renderer.cameraStickToPlayer = True

                elif event.key == pygame.K_q:  # Switch worms
                    self.world.selected_team.select_previous()
                elif event.key == pygame.K_e:
                    self.world.selected_team.select_next()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    from gameObjects import ClusterBomb
                    # self.world.explosion(*(self.renderer.cameraPosition + mouse_pos), 15)
                    self.world.entities.append(ClusterBomb(*(self.renderer.cameraPosition + mouse_pos), 0, 0))

        pressed = pygame.key.get_pressed()
        # Move camera
        if pressed[pygame.K_w]:
            self.renderer.move_camera(dt, 0, -1)
        elif pressed[pygame.K_s]:
            self.renderer.move_camera(dt, 0, 1)
        elif pressed[pygame.K_a]:
            self.renderer.move_camera(dt, -1, 0)
        elif pressed[pygame.K_d]:
            self.renderer.move_camera(dt, 1, 0)

    def update(self, dt: float):
        # Update time

        # Save data for debug screen
        if self.showDebugInfo:
            self.FPS = 1 / dt

        self.renderer.update(dt)
        self.world.update(dt)

    def draw(self, screen: pygame.Surface):
        if self.state == State.GAME_ACTIVE:
            self.renderer.draw(screen)
            if self.showTitleInGame:
                screen.blit(self.title, (screen.get_width() - self.title.get_width(), 0))
                screen.blit(self.world_name, (screen.get_width() - self.world_name.get_width(), 40))

        elif self.state == State.GAME_MENU:
            # TODO add play button to menu
            menu = self.menuFont.render("Menu", False, (255, 0, 0))
            screen.blit(menu, ((screen.get_width() - menu.get_width()) / 2, screen.get_height() / 4))

        if self.showDebugInfo:
            screen.blit(self.debugFont.render(f"FPS: {'{0:.2f}'.format(self.FPS)}", False, DEBUG_COLOR), (0, 0))
            screen.blit(
                self.debugFont.render(f"Camera stick to player: {self.renderer.cameraStickToPlayer}", False,
                                      DEBUG_COLOR),
                (0, 15))
            screen.blit(self.debugFont.render(f"Camera Position: {self.renderer.cameraPosition}", False, DEBUG_COLOR),
                        (0, 30))
            screen.blit(
                self.debugFont.render(f"Worms alive: {list(map(lambda t: t.worms_alive, self.world.wormsTeams))}",
                                      False, DEBUG_COLOR), (0, 45))
