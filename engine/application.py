import pygame

from engine.events import EventDispatcher
from .input import Input
from .layers import Layer, LayerStack
from .window import Window


class Timestep:
    def __init__(self, time: int = 0):
        self.time: int = time

    def get_seconds(self) -> float:
        return self.time / 1000

    def get_milliseconds(self) -> int:
        return self.time

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

        self.surface = pygame.display.get_surface()

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
        time = pygame.time.get_ticks()
        timestep = Timestep(int(time) - self.lastFrameTimeMillis)
        self.lastFrameTimeMillis = time

        Input.update()
        for ly in reversed(self.layerStack):
            ly.on_update(timestep)

    def on_event(self, dispatcher: EventDispatcher):
        dispatcher.dispatch(pygame.QUIT, lambda _: setattr(self, "running", False))

        for layer in self.layerStack:
            layer.on_event(dispatcher)

    def run(self):
        pygame.font.init()

        while self.running:
            self._update()
            self._render()

            self.window.on_update()
