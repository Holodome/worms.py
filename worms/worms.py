import enum

from engine import *
from worms.gameLogic.worldLoader import WorldLoader
from .gameLayer import GameLayer
from .mainMenuLayer import MainMenuLayer


class GameState(enum.Enum):
    MAIN_MENU = 1
    GAME = 2


class DebugScreenOverlay(Layer):

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self, timestep):
        self.lastTime = int(timestep)

    def on_render(self):
        if self.lastTime != 0:
            fnt = Loader.get_font("BerlinSans.TTF", 20)
            img = fnt.render("FPS: " + str(Application.Instance.fps), False, (255, 0, 0))
            Renderer2D.submit((img, (0, 0)), False)

    def on_event(self, dispatcher: EventDispatcher):
        pass


class Worms(Application):

    def __init__(self):
        Application.__init__(self, "Worms", 640, 480)

        self.currentMainLayer = MainMenuLayer()
        self.push_layer(self.currentMainLayer)
        self.push_overlay(DebugScreenOverlay())

        self.gameState: GameState = GameState.MAIN_MENU

    def on_event(self, dispatcher):
        Application.on_event(self, dispatcher)

    def start_level(self, filepath):
        self.pop_layer(self.currentMainLayer)
        world = WorldLoader.load_world_from_json(filepath)
        self.currentMainLayer = GameLayer(world)
        self.push_layer(self.currentMainLayer)
