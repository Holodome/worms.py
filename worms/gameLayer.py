from engine import *
from interface import *
from .gameLogic.world import World


class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world

        self.cameraController: CameraController = CameraController()

        self.interfaceContainer = Container(Rect(0, 0, Window.Instance.width, Window.Instance.height))
        paused_label = Label(
            Loader.get_font("ALoveOfThunder.ttf", 200).render("GAME PAUSED", False, (255, 150, 200, 245)))
        paused_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        paused_label.constraintManager.add_height_constraint(AspectConstraint())
        paused_label.constraintManager.add_x_constraint(CenterConstraint())
        paused_label.constraintManager.add_y_constraint(CenterConstraint())
        self.interfaceContainer.add_element(paused_label)

        self.paused: bool = True
        self.inAnimation = False

        self.cameraStickToEntity = True
        self.cameraFollowedEntity: Entity = self.world.sel_worm

    def on_attach(self):
        self.interfaceContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        if not self.paused:
            self.world.on_update(timestep)

            self.cameraController.on_update(timestep)
            self.cameraController.clamp_position(0, 0,
                                                 self.world.terrain.width - Window.Instance.width,
                                                 self.world.terrain.height - Window.Instance.height)

    def on_render(self):
        Renderer2D.begin_scene(self.cameraController.camera.negative_translation)
        Renderer2D.submit((self.world.backgroundImage, (0, 0)))
        Renderer2D.submit((self.world.terrain.terrainImage, (0, 0)))
        self.world.draw()
        Renderer2D.present()

        if self.paused:
            Renderer2D.RendererCommand.blend_screen(100, 100, 100, 200)
            self.interfaceContainer.on_render()

    def on_event(self, dispatcher):
        self.cameraController.on_event(dispatcher)

        dispatcher.dispatch(locals.VIDEORESIZE, lambda e: self.__setattr__("paused", True))
        dispatcher.dispatch(locals.VIDEOEXPOSE, lambda e: self.__setattr__("paused", True))

        dispatcher.dispatch(locals.KEYUP, self.on_keyup)

    def on_keyup(self, event):
        if event.key == locals.K_ESCAPE:
            self.paused = not self.paused
        elif event.key == locals.K_q:
            self.world.teamManager.sel_team.select_previous()
        elif event.key == locals.K_e:
            self.world.teamManager.sel_team.select_next()
