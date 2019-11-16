import math

import pygame

from engine import *
from engine.application import Timestep
from worms.gameLogic.gameObjects.worm import Worm
from .gameLogic.weapons import AbstractWeapon, FireData, SelectWeaponContainer
from .gameLogic.world import World
from .game_layer_misc import Crosshair, ForceBar, JumpingArrow, PauseContainer

PAUSED = 0b1000
GAMING = 0b0000
IN_ANIMATION = 0b0010
IN_WEAPON_MENU = 0b0001


class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world
        # Элементы интерфейса
        self.pauseContainer = PauseContainer()
        self.weaponMenuContainer = SelectWeaponContainer()
        # Состояние
        self.state: int = PAUSED
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
        self.fireData.shooter_position = self.world.sel_worm.pos

    def on_attach(self):
        self.world.on_update(Timestep(1))

        self.pauseContainer.set_all_visible()

        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if not self.state & IN_ANIMATION:
            self.jumpingArrow.update(float(timestep))
        else:
            if not any(map(lambda e: not isinstance(e, Worm), self.world.physicsObjects)):
                self.state -= IN_ANIMATION
                self.cameraFollowedEntity = self.world.teamManager.sel_team.sel_worm

        if not self.state & PAUSED:
            self.world.on_update(timestep)

            self.update_fire(float(timestep))
            self.forceBar.update_force_image(self.fireData.throwForce)
            if self.fireData.is_fire():
                self._fire()

            if self.cameraController.move(timestep):
                self.cameraStickToEntity = False
            if self.cameraStickToEntity:
                self.cameraController.center_to_entity(self.cameraFollowedEntity)
            self.cameraController.clamp_position(0, 0,
                                                 self.world.terrain.width - Window.Instance.width,
                                                 self.world.terrain.height - Window.Instance.height)

    def on_render(self):
        Renderer2D.begin_scene(self.cameraController.camera.negative_translation)
        self.world.draw()
        if not self.state & IN_ANIMATION:  # Если сейчас игра находится в состоянии хода одной из комманд
            # Стрелка - указатель
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
            # Прицел
            self.crosshair.draw(self.cameraFollowedEntity.pos + self.fireData.get_offset())
            # Показатель силы при стрельбе
            if self.fireData.is_active():
                self.forceBar.draw(self.cameraFollowedEntity.pos)
            # Выбранное оружие
            offset = (3, 3)
            img = self.world.teamManager.sel_team.get_weapon().HoldImage

            Renderer2D.submit(
                (pygame.transform.rotate(img, math.degrees(-self.fireData.angle) - 90),
                 self.cameraFollowedEntity.pos - offset))

        if self.state & IN_WEAPON_MENU:
            self.weaponMenuContainer.on_render()

        if self.state & PAUSED:
            self.pauseContainer.on_render()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)
        dispatcher.dispatch(plocals.KEYDOWN, self.on_keydown)

    def on_keyup(self, event):
        if event.key == plocals.K_ESCAPE:
            if self.state & PAUSED:
                self.state = GAMING
            elif self.state & GAMING:
                self.state |= PAUSED
                self.state -= GAMING

        if not self.state & PAUSED:
            if event.key == plocals.K_q:
                if not self.state & IN_ANIMATION:
                    self.select_new_worm(True)
            if event.key == plocals.K_e:
                if not self.state & IN_ANIMATION:
                    self.select_new_worm(False)
            if event.key == plocals.K_z:
                self.cameraStickToEntity = True
            if event.key == plocals.K_TAB:
                if self.state & IN_WEAPON_MENU:
                    self.state -= IN_WEAPON_MENU
                else:
                    self.state |= IN_WEAPON_MENU
            if event.key == plocals.K_SPACE:
                if self.fireData.is_active():
                    self.fireData.fireWeapon = True
        else:
            ...

    def on_keydown(self, event):
        if not self.state & PAUSED:
            if not self.state & IN_ANIMATION:
                if event.key == plocals.K_SPACE:
                    self.fireData.throwForce = 0

    def update_fire(self, dt):
        if Input.is_key_held(plocals.K_UP):
            self.fireData.update_angle(False)
        elif Input.is_key_held(plocals.K_DOWN):
            self.fireData.update_angle(True)

        if Input.is_key_held(plocals.K_SPACE) and self.fireData.is_active():
            self.fireData.update_throw_force(dt)

    def select_new_worm(self, previous: bool):
        if previous:
            self.world.teamManager.sel_team.select_previous()
        else:
            self.world.teamManager.sel_team.select_next()
        self.cameraFollowedEntity = self.world.teamManager.sel_team.sel_worm
        self.fireData.shooter_position = self.cameraFollowedEntity.pos
        self.cameraStickToEntity = True

    def _fire(self):
        weapon_class = self.world.teamManager.sel_team.get_weapon()
        self.activeWeapon = weapon_class()
        self.activeWeapon.set_data(self.fireData)
        self.activeWeapon.fire(self.world)
        self.state |= IN_ANIMATION
        self.fireData.reset()
