from engine import *
from engine.application import Timestep
from interface import *
from .gameLogic.weapons import SelectWeaponContainer
from .gameLogic.world import World


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

        self.cameraController: CameraController = CameraController()

        self.pauseContainer = PauseContainer()
        self.weaponMenuContainer = SelectWeaponContainer()

        self.paused: bool = True
        self.inAnimation: bool = False
        self.inWeaponMenu: bool = False

        self.cameraStickToEntity: bool = True
        self.cameraFollowedEntity: Entity = self.world.sel_worm

        self.jumpingArrow = JumpingArrow()

    def on_attach(self):
        self.pauseContainer.set_all_visible()

        self.weaponMenuContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if not self.paused:
            self.world.on_update(timestep)

            if not self.inAnimation:
                self.jumpingArrow.update(float(timestep))

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
        if not self.inAnimation:
            self.jumpingArrow.draw(self.cameraFollowedEntity.pos - (0, 40))

        if self.inWeaponMenu:
            self.weaponMenuContainer.on_render()

        if self.paused:
            self.pauseContainer.on_render()

        Renderer2D.present()

    def on_event(self, dispatcher):
        dispatcher.dispatch(plocals.VIDEORESIZE, lambda e: self.__setattr__("paused", True))
        dispatcher.dispatch(plocals.VIDEOEXPOSE, lambda e: self.__setattr__("paused", True))

        dispatcher.dispatch(plocals.KEYUP, self.on_keyup)

    def on_keyup(self, event):
        if event.key == plocals.K_ESCAPE:
            self.paused = not self.paused

        if not self.paused:
            if event.key == plocals.K_q:
                self.world.teamManager.sel_team.select_previous()
                self.cameraFollowedEntity = self.world.teamManager.sel_team.sel_worm
                self.cameraStickToEntity = True
            if event.key == plocals.K_e:
                self.world.teamManager.sel_team.select_next()
                self.cameraFollowedEntity = self.world.teamManager.sel_team.sel_worm
                self.cameraStickToEntity = True
            if event.key == plocals.K_z:
                self.cameraStickToEntity = True
            if event.key == plocals.K_TAB:
                self.inWeaponMenu = not self.inWeaponMenu
        else:
            ...
