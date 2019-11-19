import enum
import math

import pygame

from engine import *
from engine.application import Timestep
from .gameLayerMisc import Crosshair, ForceBar, JumpingArrow, PauseContainer
from .gameLogic.weapons import AbstractWeapon, FireData, SelectWeaponContainer
from .gameLogic.world import World


class GameState(enum.Enum):
    Paused = 1  # Игра остановлена - показывать меню паузы и не обновлять логику
    Aiming = 2  # Показывать элементы интерфейса стрельбы (прицел)
    InWeaponMenu = 3  # Показывать элементы интерфейса стрельбы а такаже меню выбора оружия
    Shooting = 4  # Убрать элементы интерфейса и ждать конца стрельбы


class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world
        # Элементы интерфейса
        self.pauseContainer = PauseContainer()
        self.weaponMenuContainer = SelectWeaponContainer()
        # Состояние
        self.state: GameState = GameState.Paused
        # Парамаетры камеры
        self.cameraController: CameraController = CameraController()
        self.cameraFollowedEntity: Entity = self.world.sel_worm
        self.cameraStickToEntity: bool = True
        # Неигровые элементы
        self.jumpingArrow = JumpingArrow()
        self.crosshair = Crosshair()
        self.forceBar = ForceBar()
        # Параметры стрельбы
        self.fireData: FireData = FireData()
        self.activeWeapon: AbstractWeapon = None
        self.fireData.shooterPosition = self.cameraFollowedEntity.pos

    def on_attach(self):
        self.world.on_update(Timestep(1))

        self.pauseContainer.set_all_visible()
        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if self.state != GameState.Shooting:
            self.jumpingArrow.update(float(timestep))
        elif self.state == GameState.Shooting:
            if self.activeWeapon is None and \
                    not any(map(lambda e: not e.is_worm(), self.world.physicsObjects)):
                self.state = GameState.Aiming
                self.cameraFollowedEntity = self.world.sel_worm

        if self.state != GameState.Paused:
            self.world.on_update(timestep)
            self.fireData.shooterPosition = self.cameraFollowedEntity.pos

            self._update_fire(float(timestep))
            self.forceBar.update_force_image(self.fireData.throwForce)
            if self.fireData.is_fire():
                self._start_weapon()
                self.fireData.fireWeapon = False
            # Обновление текущего оружия и стрельбы
            if self.activeWeapon is not None:
                if self.activeWeapon.get_valid():
                    self.activeWeapon.update(float(timestep))
                    self.activeWeapon.fire(self.world)
                else:
                    self.activeWeapon = None
                    self.fireData.reset()
            # Обновление камеры
            if self.cameraController.move(timestep):
                self.cameraStickToEntity = False
            if self.cameraStickToEntity:
                self.cameraController.center_to_entity(self.cameraFollowedEntity)
            self.cameraController.clamp_position(0, 0,
                                                 self.world.terrain.width - Window.Instance.width,
                                                 self.world.terrain.height - Window.Instance.height)

    def on_render(self):
        Renderer.begin_scene(self.cameraController.camera.negative_translation)

        self.world.draw()
        if self.state != GameState.Shooting:  # Если сейчас игра находится в состоянии хода одной из комманд
            # Стрелка - указатель
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
            # Прицел
            self.crosshair.draw(self.cameraFollowedEntity.pos + self.fireData.get_offset())
            # Показатель силы при стрельбе
            if self.fireData.is_active():
                self.forceBar.draw(self.cameraFollowedEntity.pos)

        # Выбранное оружие
        if self.state != GameState.Shooting or (self.activeWeapon is not None and self.activeWeapon.IsShooting):
            img = self.world.teamManager.sel_team.get_weapon().HoldImage
            Renderer.submit((pygame.transform.rotate(img, math.degrees(-self.fireData.angle) - 90),
                             self.cameraFollowedEntity.pos - (3, 3)))

        if self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_render()

        if self.state == GameState.Paused:
            self.pauseContainer.on_render()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)
        dispatcher.dispatch(plocals.KEYDOWN, self.on_keydown)

    def on_keyup(self, event):
        if event.key == plocals.K_ESCAPE:
            if self.state == GameState.Paused:
                self.state = GameState.Aiming
            elif self.state == GameState.Aiming:
                self.state = GameState.Paused

        if self.state != GameState.Paused:
            if event.key == plocals.K_q:
                if self.state != GameState.Shooting:
                    self._select_new_worm(True)
            if event.key == plocals.K_e:
                if self.state != GameState.Shooting:
                    self._select_new_worm(False)
            if event.key == plocals.K_z:
                self.cameraStickToEntity = True
            if event.key == plocals.K_TAB:
                if self.state == GameState.InWeaponMenu:
                    self.state = GameState.Aiming
                else:
                    self.state = GameState.InWeaponMenu
            if event.key == plocals.K_SPACE:
                if self.fireData.is_active():
                    self.fireData.fireWeapon = True

    def on_keydown(self, event):
        if self.state != GameState.Paused:
            if self.state != GameState.Shooting:
                if event.key == plocals.K_SPACE:
                    if self.world.teamManager.sel_team.get_weapon().IsThrowable:
                        self.fireData.throwForce = 0
                    else:
                        self.fireData.fireWeapon = True

    def _update_fire(self, dt):
        if Input.is_key_held(plocals.K_UP):
            self.fireData.update_angle(False)
        elif Input.is_key_held(plocals.K_DOWN):
            self.fireData.update_angle(True)

        if Input.is_key_held(plocals.K_SPACE) and self.fireData.is_active() and self.state != GameState.Shooting:
            self.fireData.update_throw_force(dt)

    def _select_new_worm(self, previous: bool):
        if previous:
            self.world.teamManager.sel_team.select_previous()
        else:
            self.world.teamManager.sel_team.select_next()
        self.cameraFollowedEntity = self.world.sel_worm
        self.cameraStickToEntity = True

    def _start_weapon(self):
        self.fireData.excludedEntities = [self.world.sel_worm]
        weapon_class = self.world.teamManager.sel_team.get_weapon()
        self.activeWeapon = weapon_class()
        self.activeWeapon.set_data(self.fireData)
        self.state = GameState.Shooting
