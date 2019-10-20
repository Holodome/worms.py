import pygame

from engine.layers import Layer
from engine.renderer.camera import CameraController
from engine.renderer.entity import Entity
from engine.renderer.scene2D import Scene2D
from .gameLogic.world import World


class GameLayer(Layer):
    def __init__(self, surface: pygame.Surface, world: World):
        self.surface: pygame.Surface = surface

        self.world: World = world

        self.cameraController: CameraController = CameraController()
        self.scene: Scene2D = Scene2D(self.cameraController.camera)
        self.scene.add_entity(Entity(self.world.backgroundImage, pygame.Vector2(0, 0)))
        self.scene.add_entity(Entity(self.world.terrain.terrainImage, pygame.Vector2(0, 0)))

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self, timestep):
        self.cameraController.on_update()

    def on_render(self):
        self.surface.fill((255, 255, 255))

        self.scene.on_render()

    def on_event(self, event):
        self.cameraController.on_event(event)
