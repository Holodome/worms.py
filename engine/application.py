import pygame

from engine.events import EventDispatcher
from engine.renderer.renderer import Renderer
from .input import Input
from .layers import Layer, LayerStack
from .window import Window


class Timestep:
    def __init__(self, time: int = 0):
        self.millis: int = time
        self.secs: float = time / 1000

    def get_seconds(self) -> float:
        return self.secs

    def get_milliseconds(self) -> int:
        return self.millis

    __float__ = get_seconds
    __int__ = get_milliseconds


class Application:
    Instance = None

    def __init__(self, title: str, width: int, height: int):
        Application.Instance = self

        self.window: Window = Window(title, width, height)
        self.window.eventCallback = self.on_event

        self.layerStack: LayerStack = LayerStack()

        self.lastFrameTimeMillis: int = 0

        self.running: bool = True

        self.fixedFPS = 100

        self.fpsQueue = [0] * 60
        self.fps = 0
        self.clock = pygame.time.Clock()

    def push_layer(self, layer: Layer):
        self.layerStack.push_layer(layer)

    def push_overlay(self, layer: Layer):
        self.layerStack.push_overlay(layer)

    def pop_layer(self, layer: Layer):
        self.layerStack.pop_layer(layer)

    def pop_overlay(self, layer: Layer):
        self.layerStack.pop_overlay(layer)

    def _render(self):
        for ly in self.layerStack:
            ly.on_render()

    def _update(self):
        dt = self.clock.tick(self.fixedFPS)

        if dt != 0:
            self.fpsQueue.pop(0)
            self.fpsQueue.append(1000 // dt)
            self.fps = sum(self.fpsQueue) // 60

        Input.update()
        for ly in reversed(self.layerStack):
            ly.on_update(Timestep(dt % (50)))

    def on_event(self, dispatcher: EventDispatcher):
        dispatcher.dispatch(pygame.QUIT, lambda _: setattr(self, "running", False))

        for layer in self.layerStack:
            layer.on_event(dispatcher)

    def run(self):
        while self.running:
            self._update()

            Renderer.start_frame()
            self._render()

            Renderer.present()
            self.window.on_update()
