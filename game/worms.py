import math

import pygame

from toolbox import loader
from toolbox.event import Input
from world.world_loader import load_from_json
from world.world_renderer import WorldRenderer

DEBUG_COLOR = (50, 50, 50)
debugFont = loader.get_font("Consolas", 15)

title = loader.get_font("RubberBiscuitItalic.TTF", 40).render("WORMS.PY", False, (30, 30, 30))

GAME_ACTIVE = 0b0001
GAME_PAUSED = 0b0010
GAME_MENU = 0b0100


class Worms:

    def __init__(self, screen_size):
        self.screenSize = screen_size
        self.state = GAME_ACTIVE

        self.input = Input(screen_size)

        self.world = load_from_json("res/levels/bikini_bottom.json")
        self.renderer = WorldRenderer(self.world, screen_size)

        self.world_name = loader.get_font("RubberBiscuitBold.TTF", 20).render(self.world.name, False, (50, 50, 50))

        self.showDebugInfo: bool = False
        self.fullscreen: bool = False
        self.inWeaponMenu: bool = False

        self.FPS: float = 0

        self.throwForce = -1  # Change to 0 for start
        self.fireWeapon = False

    def event(self, dt: float):
        if self.input.update():
            self.state = GAME_PAUSED

        if self.input.key_is_released(pygame.K_ESCAPE) and self.state != GAME_MENU:
            self.state = GAME_ACTIVE if self.state == GAME_PAUSED else GAME_PAUSED
        if self.input.key_is_released(pygame.K_F3):
            self.showDebugInfo = not self.showDebugInfo
        elif self.input.key_is_released(pygame.K_F11):
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                pygame.display.set_mode(flags=pygame.HWSURFACE | pygame.FULLSCREEN)
            else:
                pygame.display.set_mode()

        if self.state == GAME_ACTIVE:
            if self.input.key_is_pressed(pygame.K_SPACE) and self.renderer.notInAnimation:
                self.throwForce = 0

            if self.input.key_is_released(pygame.K_F2):
                self.world.debrisAllowed = not self.world.debrisAllowed
            # Switch time to detonation
            elif self.input.key_is_released(pygame.K_1):
                self.world.team_manager.selected_weapon_manager.time = 1
            elif self.input.key_is_released(pygame.K_2):
                self.world.team_manager.selected_weapon_manager.time = 2
            elif self.input.key_is_released(pygame.K_3):
                self.world.team_manager.selected_weapon_manager.time = 3
            elif self.input.key_is_released(pygame.K_4):
                self.world.team_manager.selected_weapon_manager.time = 4
            elif self.input.key_is_released(pygame.K_5):
                self.world.team_manager.selected_weapon_manager.time = 5

            elif self.input.key_is_released(pygame.K_TAB):
                self.inWeaponMenu = not self.inWeaponMenu
                if self.inWeaponMenu:
                    pygame.mouse.set_visible(True)
                else:
                    pygame.mouse.set_visible(False)
            elif self.throwForce != -1 and self.input.key_is_released(pygame.K_SPACE):
                self.fireWeapon = True
            elif self.input.key_is_released(pygame.K_r):
                self.renderer.cameraStickToPlayer = True
            elif self.input.key_is_released(pygame.K_q):
                self.renderer.cameraTrackingEntity = self.world.team_manager.selected_team.select_previous()
            elif self.input.key_is_released(pygame.K_e):
                self.renderer.cameraTrackingEntity = self.world.team_manager.selected_team.select_next()

            if self.input.key_is_held(pygame.K_w):
                self.renderer.move_camera(dt, 0, -1)
            elif self.input.key_is_held(pygame.K_s):
                self.renderer.move_camera(dt, 0, 1)
            if self.input.key_is_held(pygame.K_a):
                self.renderer.move_camera(dt, -1, 0)
            elif self.input.key_is_held(pygame.K_d):
                self.renderer.move_camera(dt, 1, 0)

            if self.input.key_is_held(pygame.K_UP):  # Move shooting angle anti-clockwise
                self.world.team_manager.selected_weapon_manager.shootingAngle -= math.pi / 1000
            elif self.input.key_is_held(pygame.K_DOWN):  # Move shooting angle clockwise
                self.world.team_manager.selected_weapon_manager.shootingAngle += math.pi / 1000

            if self.input.key_is_held(pygame.K_SPACE) and self.throwForce != -1:  # Add force to shot
                self.throwForce += dt
                if self.throwForce > 1:
                    self.throwForce = 1
                    self.fireWeapon = True

            if self.input.button_is_released(1):  # LMC
                if self.inWeaponMenu:
                    self.world.team_manager.selected_weapon_manager.select_weapon(
                        self.input.x * self.screenSize[0],
                        self.input.y * self.screenSize[1],
                        self.screenSize[1])

        elif self.state == GAME_MENU:
            pass

        elif self.state == GAME_PAUSED:
            self.renderer.update(dt)

    def update(self, dt: float):
        if self.state & GAME_ACTIVE:
            if self.showDebugInfo:
                self.FPS = 1 / dt

            if self.fireWeapon:
                fired_entities = self.world.team_manager.selected_weapon_manager \
                    .fire(*self.world.team_manager.selected_team.selected_worm.position, self.throwForce)
                self.renderer.set_weapon_fired(fired_entities[0])
                self.world.entities.extend(fired_entities)
                self.fireWeapon = False
                self.throwForce = -1

            self.renderer.update(dt)
            self.world.update(dt)

        elif self.state == GAME_MENU:
            pass

    def draw(self, screen: pygame.Surface):
        if self.state == GAME_ACTIVE:
            self.renderer.draw(screen)
            if self.throwForce != -1:
                self.renderer.draw_force_bar(screen, self.throwForce)
            if self.inWeaponMenu:
                self.world.team_manager.selected_weapon_manager.draw_menu(screen, *self.screenSize)

        elif self.state == GAME_MENU:
            pass

        elif self.state == GAME_PAUSED:
            self.renderer.draw(screen)
            img = loader.get_font("ALoveOfThunder.ttf", 80).render("GAME PAUSED", False, (255, 150, 200, 245))
            screen.blit(img,
                        ((self.screenSize[0] - img.get_width()) // 2, (self.screenSize[1] - img.get_height()) // 2))
            screen.blit(title, (screen.get_width() - title.get_width(), 10))
            screen.blit(self.world_name, (screen.get_width() - self.world_name.get_width(), 60))

        if self.showDebugInfo:
            screen.blit(debugFont.render(f"FPS: {'{0:.2f}'.format(self.FPS)}", False, DEBUG_COLOR), (0, 0))
            screen.blit(debugFont.render(f"Camera Position: {self.renderer.cameraPosition}", False, DEBUG_COLOR),
                        (0, 15))
            screen.blit(
                debugFont.render(f"Worms alive: {list(map(lambda t: t.worms_alive, self.world.team_manager.number_of_teams))}",
                                 False, DEBUG_COLOR), (0, 30))
