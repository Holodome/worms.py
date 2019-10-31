import os
from typing import Callable

import pygame

from engine.events import EventDispatcher

_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF  # | pygame.RESIZABLE  # !!! Not Working Properly
if pygame.vernum[0] >= 2:
    _MODE |= pygame.SCALED


class Window:
    Instance = None

    def __init__(self, title: str, width: int, height: int):
        Window.Instance = self

        self.title = title
        self.width = width
        self.height = height

        self.fullscreen = False

        self.eventCallback: Callable[[pygame.event.EventType], bool] = lambda event: False

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_mode((width, height), _MODE)
        pygame.display.set_caption(title)

        # pygame.mouse.set_visible(False)

    def on_update(self):
        pygame.display.flip()
        self._poll_events()

    def _poll_events(self):
        for event in pygame.event.get():
            setattr(event, "Handled", False)
            dispatcher = EventDispatcher(event)
            dispatcher.dispatch(pygame.VIDEORESIZE, lambda e: pygame.display.set_mode(e.size, _MODE))
            self.eventCallback(dispatcher)

    @staticmethod
    def get_surface():
        return pygame.display.get_surface()
