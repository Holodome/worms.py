import pygame

from engine.input import Input
from engine.layers import Layer
from engine.renderer.camera import CameraController
from engine.renderer.entity import Entity
from engine.renderer.scene2D import Scene2D
from engine.window import Window
from .gameLogic.world import World


class GameLayer(Layer):
    def __init__(self, surface: pygame.Surface, world: World):
        self.surface: pygame.Surface = surface

        self.world: World = world

        self.cameraController: CameraController = CameraController()
        self.scene: Scene2D = Scene2D(self.cameraController.camera)

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self, timestep):
        self.world.on_update(timestep)

        self.cameraController.on_update(timestep)
        self.cameraController.clamp_position(0, 0,
                                             self.world.terrain.width - Window.Instance.width,
                                             self.world.terrain.height - Window.Instance.height)

    def on_render(self):
        self.surface.fill((255, 255, 255))

        self.scene.entities.clear()
        self.scene.add(Entity(self.world.backgroundImage, pygame.Vector2(0, 0)))
        self.scene.add(Entity(self.world.terrain.terrainImage, pygame.Vector2(0, 0)))
        self.scene.entities.extend(self.world.physicsObjects)

        self.scene.on_render()

    def on_event(self, dispatcher):
        self.cameraController.on_event(dispatcher)

        if dispatcher.event.type == pygame.MOUSEBUTTONUP:
            x, y = Input.get_mouse_pos()
            x += self.cameraController.camera.x
            y += self.cameraController.camera.y
            self.world.explosion(int(x), int(y), 15, 10, 1)

