import numpy
import pygame

from .world import World


class Camera:
    def __init__(self):
        self.position: numpy.ndarray = numpy.zeros(2, dtype=numpy.uint32)

    def get_offset(self):
        return -int(self.position[0]), -int(self.position[0])

    def on_update(self):
        pass


class WorldRenderer:
    def __init__(self, world: World):
        self.world = world

        self.camera: Camera = Camera()

    def on_update(self):
        self.camera.on_update()

    def on_render(self, surface: pygame.Surface):
        pass

    def on_event(self, event):
        pass
