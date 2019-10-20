import pygame

from .events import EventDispatcher
from .layers import Layer, LayerStack
from .window import Window
from .input import Input

RENDER = pygame.USEREVENT + 1
UPDATE = pygame.USEREVENT + 2


class Timestep:
    def __init__(self, time: float = 0.0):
        self.time = time

    def get_seconds(self):
        return self.time

    def get_milliseconds(self):
        return self.time * 1000

    __float__ = get_seconds
    __int__ = get_milliseconds


class Application:
    Instance = None

    def __init__(self, title: str, width: int, height: int):
        Application.Instance = self

        self.window: Window = Window(title, width, height)
        self.window.eventCallback = self.on_event

        self.layerStack: LayerStack = LayerStack()

        self.lastFrameTime: float = 0.0
        self.timestep = Timestep(0)

        self.running = True

        self.surface = pygame.display.get_surface()

    def push_layer(self, layer: Layer):
        self.layerStack.push_layer(layer)

    def push_overlay(self, layer: Layer):
        self.layerStack.push_overlay(layer)

    def pop_layer(self, layer: Layer):
        self.layerStack.pop_layer(layer)

    def pop_overlay(self, layer: Layer):
        self.layerStack.pop_overlay(layer)

    def _render(self, _):
        for ly in self.layerStack:
            ly.on_render()

    def _update(self, _):
        Input.update()
        for ly in self.layerStack:
            ly.on_update(self.timestep)

    def on_event(self, dispatcher: pygame.event.EventType):
        dispatcher.dispatch(pygame.QUIT, lambda _: setattr(self, "running", False))
        dispatched = dispatcher.dispatch(UPDATE, self._update)
        dispatched = dispatcher.dispatch(RENDER, self._render) or dispatched

        if dispatched:
            return

        for layer in self.layerStack:
            layer.on_event(dispatcher)

    def run(self):
        pygame.time.set_timer(RENDER, 1000 // 60)
        pygame.time.set_timer(UPDATE, 1000 // 60)

        pygame.font.init()

        while self.running:
            time = pygame.time.get_ticks()
            self.timestep = Timestep(time - self.lastFrameTime)
            self.lastFrameTime = time
            self.window.on_update()
