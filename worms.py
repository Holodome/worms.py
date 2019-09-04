import enum
import math
import os
import sys

import pygame

import loader
from world import WorldRenderer, load_from_json

DEBUG_COLOR = (50, 50, 50)
titleFont = loader.get_font("title.TTF", 40)
worldFont = loader.get_font("worldName.TTF", 20)
debugFont = loader.get_font("Consolas", 15)

title = titleFont.render("WORMS.PY", False, (30, 30, 30))


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

    def __init__(self, screen_size):
        # Game state
        self.state: State = State.GAME_ACTIVE
        # World and its renderer
        self.world = load_from_json("res/levels/bikini_bottom.json")
        self.renderer = WorldRenderer(self.world, screen_size)

        self.world_name = worldFont.render(self.world.name, False, (100, 100, 100))

        self.showDebugInfo: bool = False
        self.showTitleInGame: bool = True
        self.fullscreen: bool = False
        self.inWeaponMenu: bool = False
        # Temporary data
        self.FPS: float = 0

        self.throwForce = -1  # Change to 0 for start
        self.fireWeapon = False

    def event(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.throwForce = 0

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.world.debrisAllowed = not self.world.debrisAllowed
                elif event.key == pygame.K_F3:
                    self.showDebugInfo = not self.showDebugInfo
                elif event.key == pygame.K_F4:
                    self.showTitleInGame = not self.showTitleInGame
                elif event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        pygame.display.set_mode(flags=pygame.HWSURFACE | pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode()

                elif event.key == pygame.K_TAB:
                    self.inWeaponMenu = not self.inWeaponMenu
                    if self.inWeaponMenu:
                        pygame.mouse.set_visible(True)
                    else:
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_SPACE and self.throwForce != -1:
                    self.fireWeapon = True

                elif event.key == pygame.K_r:
                    self.renderer.cameraStickToPlayer = True
                elif event.key == pygame.K_q:
                    self.renderer.cameraTrackingEntity = self.world.selected_team.select_previous()
                elif event.key == pygame.K_e:
                    self.renderer.cameraTrackingEntity = self.world.selected_team.select_next()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass

        # Move camera
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.renderer.move_camera(dt, 0, -1)
        if pressed[pygame.K_s]:
            self.renderer.move_camera(dt, 0, 1)
        if pressed[pygame.K_a]:
            self.renderer.move_camera(dt, -1, 0)
        if pressed[pygame.K_d]:
            self.renderer.move_camera(dt, 1, 0)

        if pressed[pygame.K_UP]:  # Move shooting angle anti-clockwise
            self.world.selected_team.weapon_manager.shootingAngle -= math.pi / 1000
        if pressed[pygame.K_DOWN]:  # Move shooting angle clockwise
            self.world.selected_team.weapon_manager.shootingAngle += math.pi / 1000
        if pressed[pygame.K_LEFT]:  # Move worm left
            pass
        if pressed[pygame.K_RIGHT]:  # Move worm right
            pass

        if pressed[pygame.K_SPACE] and self.throwForce != -1:  # Add force to shot
            self.throwForce += dt
            if self.throwForce > 1:
                self.throwForce = 1
                self.fireWeapon = True

    def update(self, dt: float):
        # Save data for debug screen
        if self.showDebugInfo:
            self.FPS = 1 / dt

        if self.fireWeapon:
            ent = self.world.selected_team.weapon_manager.fire(self.world, self.throwForce)
            self.fireWeapon = False
            self.throwForce = -1

            self.renderer.set_weapon_fired(ent[0])
            self.world.entities.extend(ent)

        self.renderer.update(dt)
        self.world.update(dt)

    def draw(self, screen: pygame.Surface):
        if self.state == State.GAME_ACTIVE:
            self.renderer.draw(screen)
            if self.throwForce != -1:
                self.renderer.draw_force_bar(screen, self.throwForce)

            if self.showTitleInGame:
                screen.blit(title, (screen.get_width() - title.get_width(), 0))
                screen.blit(self.world_name, (screen.get_width() - self.world_name.get_width(), 40))

        elif self.state == State.GAME_MENU:
            pass

        if self.showDebugInfo:
            screen.blit(debugFont.render(f"FPS: {'{0:.2f}'.format(self.FPS)}", False, DEBUG_COLOR), (0, 0))
            screen.blit(debugFont.render(f"Camera Position: {self.renderer.cameraPosition}", False, DEBUG_COLOR),
                        (0, 15))
            screen.blit(
                debugFont.render(f"Worms alive: {list(map(lambda t: t.worms_alive, self.world.wormsTeams))}",
                                 False, DEBUG_COLOR), (0, 30))
