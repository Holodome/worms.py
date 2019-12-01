import enum
import math

from engine import *
from engine.application import Timestep
from worms.gameLogic.gameObjects.physicsObject import PhysicsObject
from .gameLayerMisc import Crosshair, ForceBar, JumpingArrow, PauseContainer
from .gameLogic.weapons import AbstractWeapon, FireData, SelectWeaponContainer, SetData
from .gameLogic.world import World

JUMP_COEF = 30


class GameState(enum.Enum):
    Paused = 1  # Игра остановлена - показывать меню паузы и не обновлять логику
    Aiming = 2  # Показывать элементы интерфейса стрельбы (прицел)
    InWeaponMenu = 3  # Показывать элементы интерфейса стрельбы а такаже меню выбора оружия
    Shooting = 4  # Убрать элементы интерфейса и ждать конца стрельбы
    ZoomedOut = 5
    Walking = 6  # Тоже самое, что прицеливание, но без показа оружия и прыжком вместо стрельбы


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
        self.cameraFollowedEntity: PhysicsObject = self.world.sel_worm
        self.cameraStickToEntity: bool = True
        # Неигровые элементы
        self.jumpingArrow = JumpingArrow()
        self.crosshair = Crosshair()
        self.forceBar = ForceBar()
        # Параметры стрельбы
        self.fireData: FireData = FireData()
        self.activeWeapon: AbstractWeapon = None

    def on_attach(self):
        self.world.on_update(Timestep(1))

        self.pauseContainer.set_all_visible()
        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_update()
            self.world.teamManager.sel_team.selectedWeaponId = self.weaponMenuContainer.lastSelectedWeaponID

        if self.state != GameState.Shooting:
            self.jumpingArrow.update(float(timestep))
        elif self.state == GameState.Shooting:
            if self.activeWeapon is None \
                    and not any(map(lambda e: not e.is_worm(), self.world.physicsObjects)):
                self.state = GameState.Aiming
                self.cameraFollowedEntity = self.world.sel_worm

        if self.state != GameState.Paused:
            self.world.on_update(timestep)
            self.fireData.shooterPosition = self.cameraFollowedEntity.pos
            SetData(self.fireData)

            self._update_fire(float(timestep))
            self.forceBar.update_force_image(self.fireData.throwForce)
            if self.fireData.is_fire():
                if self.state == GameState.Aiming:
                    self._start_weapon()
                elif self.state == GameState.Walking:
                    self.jump_worm()
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
        if self.state == GameState.Paused:
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
        elif self.state == GameState.Aiming:
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
            self.crosshair.draw(self.cameraFollowedEntity.pos + self.fireData.get_offset())
            if self.fireData.is_active():
                self.forceBar.draw(self.cameraFollowedEntity.pos)
            self.world.teamManager.sel_team.get_weapon().draw_hold()
        elif self.state == GameState.Walking:
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
            self.crosshair.draw(self.cameraFollowedEntity.pos + self.fireData.get_offset())
            if self.fireData.is_active():
                self.forceBar.draw(self.cameraFollowedEntity.pos)
        elif self.state == GameState.InWeaponMenu:
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos)
            self.world.teamManager.sel_team.get_weapon().draw_hold()
        elif self.state == GameState.Shooting:
            if self.activeWeapon is not None and self.activeWeapon.IsShooting:
                self.world.teamManager.sel_team.get_weapon().draw_hold()

        if self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_render()

        if self.state == GameState.Paused:
            self.pauseContainer.on_render()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)
        dispatcher.dispatch(plocals.KEYDOWN, self.on_keydown)

        if self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_event(dispatcher)

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
            elif event.key == plocals.K_e:
                if self.state != GameState.Shooting:
                    self._select_new_worm(False)
            elif event.key == plocals.K_z:
                self.cameraStickToEntity = True
            elif event.key == plocals.K_TAB:
                if self.state == GameState.InWeaponMenu:
                    self.state = GameState.Aiming
                else:
                    self.state = GameState.InWeaponMenu
            elif event.key == plocals.K_SPACE:
                if self.fireData.is_active():
                    self.fireData.fireWeapon = True
            elif event.key == plocals.K_LCTRL:
                if self.state == GameState.Walking:
                    self.state = GameState.Aiming
                elif self.state == GameState.Aiming:
                    self.state = GameState.Walking
            elif event.key == plocals.K_1:
                self.fireData.timeToExplode = 1
                self.weaponMenuContainer.set_time(1)
            elif event.key == plocals.K_2:
                self.fireData.timeToExplode = 2
                self.weaponMenuContainer.set_time(2)
            elif event.key == plocals.K_3:
                self.fireData.timeToExplode = 3
                self.weaponMenuContainer.set_time(3)
            elif event.key == plocals.K_4:
                self.fireData.timeToExplode = 4
                self.weaponMenuContainer.set_time(4)
            elif event.key == plocals.K_5:
                self.fireData.timeToExplode = 5
                self.weaponMenuContainer.set_time(5)

    def on_keydown(self, event):
        if self.state != GameState.Paused:
            if self.state != GameState.Shooting:
                if event.key == plocals.K_SPACE:
                    if self.cameraFollowedEntity.stable:
                        if self.world.teamManager.sel_team.get_weapon().IsThrowable:
                            self.fireData.throwForce = 0
                        else:
                            self.fireData.fireWeapon = True

    def _update_fire(self, dt):
        if Input.is_key_held(plocals.K_UP):
            self.fireData.update_angle(False)
        elif Input.is_key_held(plocals.K_DOWN):
            self.fireData.update_angle(True)

        if Input.is_key_held(plocals.K_SPACE) \
                and self.fireData.is_active() \
                and self.state != GameState.Shooting:
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

    def jump_worm(self):
        worm = self.world.sel_worm
        vx = math.cos(self.fireData.angle) * JUMP_COEF * self.fireData.throwForce
        vy = math.sin(self.fireData.angle) * JUMP_COEF * self.fireData.throwForce
        worm.vel_x += vx
        worm.vel_y += vy
        self.fireData.reset()
