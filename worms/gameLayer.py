import pygame

from engine.input import Input
from engine.layers import Layer
from engine.loader import Loader
from engine.renderer.camera import CameraController
from engine.renderer.entity import Entity
from engine.renderer.renderer2D import Renderer2D
from engine.renderer.scene2D import Scene2D
from engine.window import Window
from .gameLogic.world import World

from interface import *

class GameLayer(Layer):
    def __init__(self, world: World):
        self.world: World = world

        self.cameraController: CameraController = CameraController()
        self.scene: Scene2D = Scene2D(self.cameraController.camera)

        self.paused: bool = True

        self.interfaceContainer = Container(pygame.Rect(0, 0, Window.Instance.width, Window.Instance.height))
        paused_label = Label(Loader.get_font("ALoveOfThunder.ttf", 200).render("GAME PAUSED", False, (255, 150, 200, 245)))
        paused_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        paused_label.constraintManager.add_height_constraint(AspectConstraint())
        paused_label.constraintManager.add_x_constraint(CenterConstraint())
        paused_label.constraintManager.add_y_constraint(CenterConstraint())
        self.interfaceContainer.add_element(paused_label)

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
        self.scene.entities.clear()
        self.scene.add(Entity(self.world.backgroundImage, pygame.Vector2(0, 0)))
        self.scene.add(Entity(self.world.terrain.terrainImage, pygame.Vector2(0, 0)))
        self.scene.entities.extend(self.world.physicsObjects)

        self.scene.on_render()

        if self.paused:
            Renderer2D.RendererCommand.blend_screen(100, 100, 100, 200)
            self.interfaceContainer.on_render()


    def on_event(self, dispatcher):
        self.cameraController.on_event(dispatcher)

        dispatcher.dispatch(pygame.VIDEORESIZE, lambda e: self.__setattr__("paused", True))
        dispatcher.dispatch(pygame.VIDEOEXPOSE, lambda e: self.__setattr__("paused", True))

        dispatcher.dispatch(pygame.KEYUP, lambda e:
        [self.__setattr__("paused", not self.paused)] if e.key == pygame.K_ESCAPE else None)
        # TODO : remove
        if dispatcher.event.type == pygame.MOUSEBUTTONUP:
            x, y = Input.get_mouse_pos()
            x += self.cameraController.camera.x
            y += self.cameraController.camera.y
            self.world.explosion(int(x), int(y), 15, 10, 1)
