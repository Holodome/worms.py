import math

from engine import *
from engine.application import Timestep
from interface import *
from worms.gameLogic.gameObjects.worm import Worm
from .gameLogic.weapons import FireData, SelectWeaponContainer, get_force_bar
from .gameLogic.world import World

CROSSHAIR_IMAGE = Loader.load_image("crosshair")

FORCE_BAR_OFFSET = (-4, 25)
JUMPING_ARROW_OFFSET = (0, 40)


class JumpingArrow:

    def __init__(self):
        self.image = Loader.load_image("arrow")

        self.vertPos: float = 5
        self.goingUp: bool = True

    def update(self, dt):
        self.vertPos = clamp(self.vertPos + (self.goingUp or -1) * 10 * dt, 0, 5)
        if self.vertPos == 5 or self.vertPos == 0:
            self.goingUp = not self.goingUp

    def draw(self, position):
        Renderer2D.submit((self.image, vec_to_itup(position + (0, int(self.vertPos ** 2) - 25))))


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


class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world
        self.world.on_update(Timestep(1))

        # Элементы интерфейса
        self.pauseContainer = PauseContainer()
        self.weaponMenuContainer = SelectWeaponContainer()
        # Состояния
        self.paused: bool = True
        self.inAnimation: bool = False
        self.inWeaponMenu: bool = False
        # Парамаетры камеры
        self.cameraStickToEntity: bool = True
        self.cameraFollowedEntity: Entity = self.world.sel_worm
        self.cameraController: CameraController = CameraController()

        self.jumpingArrow = JumpingArrow()

        self.fireData = FireData()

    def on_attach(self):
        self.pauseContainer.set_all_visible()

        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if not self.inAnimation:
            self.jumpingArrow.update(float(timestep))
        else:
            if not any(map(lambda e: not isinstance(e, Worm), self.world.physicsObjects)):
                self.inAnimation = False
                self.cameraFollowedEntity = self.world.teamManager.sel_team.sel_worm

        if not self.paused:
            self.world.on_update(timestep)

            self.update_fire(float(timestep))
            if self.fireData.is_fire():
                bullet_class = self.world.teamManager.sel_team.weaponManager.get_weapon().bullet
                print(self.fireData.angle, self.fireData.throwForce)
                bullet = bullet_class(self.world.teamManager.sel_team.weaponManager.timeToExplode,
                                      *self.cameraFollowedEntity.pos)
                bullet.vel_x = math.cos(self.fireData.angle) * self.fireData.throwForce * 50
                bullet.vel_y = math.sin(self.fireData.angle) * self.fireData.throwForce * 50
                self.world.physicsObjects.append(bullet)
                self.inAnimation = True
                self.fireData.reset()

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
        if not self.inAnimation:  # Если сейчас игра находится в состоянии хода одной из комманд
            # Стрелка - указатель
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos - JUMPING_ARROW_OFFSET)
            # Прицел
            Renderer2D.submit((CROSSHAIR_IMAGE, self.cameraFollowedEntity.pos +
                               self.fireData.get_offset()))
            # Показатель силы при стрельбе
            if self.fireData.is_active():
                Renderer2D.submit((get_force_bar(self.fireData.throwForce),
                                   vec_to_itup(self.cameraFollowedEntity.pos + FORCE_BAR_OFFSET)))
            # Выбранное оружие
            offset = (7, -2) if not self.cameraFollowedEntity.headedRight else (-13, -2)
            Renderer2D.submit(
                (self.world.teamManager.sel_team.weaponManager.get_weapon().holdImage,
                 vec_to_itup(self.cameraFollowedEntity.pos - offset)))

        if self.inWeaponMenu:
            self.weaponMenuContainer.on_render()

        if self.paused:
            self.pauseContainer.on_render()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)
        dispatcher.dispatch(plocals.KEYDOWN, self.on_keydown)

    def on_keyup(self, event):
        if event.key == plocals.K_ESCAPE:
            self.paused = not self.paused

        if not self.paused:
            if event.key == plocals.K_q:
                if not self.inAnimation:
                    self.select_new_worm(True)
            if event.key == plocals.K_e:
                if not self.inAnimation:
                    self.select_new_worm(False)
            if event.key == plocals.K_z:
                self.cameraStickToEntity = True
            if event.key == plocals.K_TAB:
                self.inWeaponMenu = not self.inWeaponMenu
            if event.key == plocals.K_SPACE:
                if self.fireData.is_active():
                    self.fireData.fireWeapon = True
        else:
            ...

    def on_keydown(self, event):
        if not self.paused:
            if not self.inAnimation:
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
        self.cameraStickToEntity = True
