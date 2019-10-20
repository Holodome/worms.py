import enum

import pygame

from engine.application import Application
from worms.gameLogic.worldLoader import WorldLoader
from .gameLayer import GameLayer
from .mainMenuLayer import MainMenuLayer


class GameState(enum.Enum):
    MAIN_MENU = 1
    GAME = 2


class Worms(Application):

    def __init__(self):
        Application.__init__(self, "Worms", 640, 480)

        self.currentMainLayer = MainMenuLayer(self.surface)
        self.push_layer(self.currentMainLayer)

        self.gameState: GameState = GameState.MAIN_MENU

    def on_event(self, dispatcher: pygame.event.EventType):
        Application.on_event(self, dispatcher)

    def start_level(self, filepath):
        self.pop_layer(self.currentMainLayer)
        world = WorldLoader.load_world_from_json(filepath)
        self.currentMainLayer = GameLayer(self.surface, world)
        self.push_layer(self.currentMainLayer)