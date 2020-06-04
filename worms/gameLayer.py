import enum
import math

from engine import *
from engine.application import Timestep
from worms.gameLogic.gameObjects.physicsObject import PhysicsObject
from .gameLayerMisc import Crosshair, ForceBar, JumpingArrow, PauseContainer, EndGameContainer
from .gameLogic.weapons import AbstractWeapon, FireData, SelectWeaponContainer, SetData
from .gameLogic.world import World

JUMP_COEF = 30


class GameState(enum.Enum):
    Paused = 1  # Игра остановлена - показывать меню паузы и не обновлять логику
    Aiming = 2  # Показывать элементы интерфейса стрельбы (прицел)
    InWeaponMenu = 3  # Показывать элементы интерфейса стрельбы а такаже меню выбора оружия
    Shooting = 4  # Убрать элементы интерфейса и ждать конца стрельбы
    Walking = 5  # Тоже самое, что прицеливание, но без показа оружия и прыжком вместо стрельбы

    GameEnded = 6  # Прекратить обновлние игры, отрисовывать меню с информацией о окончании игры и кнопки выхода


class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world
        # Элементы интерфейса
        self.pauseContainer = PauseContainer()
        self.weaponMenuContainer = SelectWeaponContainer()
        self.endGameContainer = EndGameContainer()
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
        self.endGameContainer.set_all_visible()
        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if self.state == GameState.GameEnded:
            self.endGameContainer.on_update()
            return

        if self.state != GameState.Paused:
            if self.world.teamManager.get_no_enemies_left():
                self.state = GameState.GameEnded
                return

        if self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_update()
            self.world.teamManager.sel_team.selectedWeaponId = self.weaponMenuContainer.lastSelectedWeaponID
        if self.state != GameState.Shooting:
            self.jumpingArrow.update(float(timestep))
            if not self.cameraFollowedEntity.Alive:
                self._select_new_worm(False)
        else:
            if self.activeWeapon is None \
                    and all(map(lambda e: e.stable, self.world.physicsObjects)):
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
                    self._jump_worm()
                self.fireData.end_fire()

            # Обновление текущего оружия и стрельбы
            if self.activeWeapon is not None:
                if self.activeWeapon.get_valid():
                    self.activeWeapon.update(float(timestep))
                    self.activeWeapon.fire(self.world)
                else:
                    self.activeWeapon = None
                    self.fireData.reset()
                    self.pass_turn()

            # Обновление камеры
            if self.cameraController.move(timestep):
                self.cameraStickToEntity = False
            if self.cameraStickToEntity:
                self.cameraController.center_to_entity(self.cameraFollowedEntity)
            self.cameraController.clamp_position(0, 0,
                                                 self.world.terrain.width - Window.Instance.width,
                                                 self.world.terrain.height - Window.Instance.height)
        else:
            self.pauseContainer.on_update()


    def on_render(self):
        Renderer.begin_scene(self.cameraController.camera.negative_translation)

        self.world.draw()
        if self.state == GameState.GameEnded:
            self.endGameContainer.on_render()
        elif self.state == GameState.Paused:
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

        if self.state == GameState.Paused:
            self.pauseContainer.on_render()
        else:
            if self.state == GameState.InWeaponMenu:
                self.weaponMenuContainer.on_render()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)
        dispatcher.dispatch(plocals.KEYDOWN, self.on_keydown)

        if self.state == GameState.Paused:
            self.pauseContainer.on_event(dispatcher)
        elif self.state == GameState.InWeaponMenu:
            self.weaponMenuContainer.on_event(dispatcher)
        elif self.state == GameState.GameEnded:
            self.endGameContainer.on_event(dispatcher)

    def on_keyup(self, event):
        if event.key == plocals.K_ESCAPE:
            self.switch_states(GameState.Paused, GameState.Aiming)

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
                self.switch_states(GameState.InWeaponMenu, GameState.Aiming)
            elif event.key == plocals.K_SPACE:
                if self.fireData.is_active():
                    self.fireData.fireWeapon = True
            elif event.key == plocals.K_LCTRL:
                self.switch_states(GameState.Walking, GameState.Aiming)
            elif event.key == plocals.K_1:
                self._change_exp_time(1)
            elif event.key == plocals.K_2:
                self._change_exp_time(2)
            elif event.key == plocals.K_3:
                self._change_exp_time(3)
            elif event.key == plocals.K_4:
                self._change_exp_time(4)
            elif event.key == plocals.K_5:
                self._change_exp_time(5)

    def on_keydown(self, event):
        if event.key == plocals.K_SPACE:
            if self.state == GameState.Aiming:
                if self.cameraFollowedEntity.stable:
                    if self.world.teamManager.sel_team.get_weapon().IsThrowable:
                        self.fireData.throwForce = 0
                    else:
                        self.fireData.fireWeapon = True
            elif self.state == GameState.Walking:
                self.fireData.throwForce = 0

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

    def _jump_worm(self):
        worm = self.world.sel_worm
        vx = math.cos(self.fireData.angle) * JUMP_COEF * self.fireData.throwForce
        vy = math.sin(self.fireData.angle) * JUMP_COEF * self.fireData.throwForce
        worm.vel_x += vx
        worm.vel_y += vy
        self.fireData.reset()

    def _change_exp_time(self, time):
        self.fireData.timeToExplode = time
        self.weaponMenuContainer.set_time(time)

    def switch_states(self, a, b):
        if self.state == a:
            self.state = b
        elif self.state == b:
            self.state = a

    def pass_turn(self):
        self.world.teamManager.pass_turn()
