import pygame

from engine.layers import Layer
from engine.loader import Loader
from interface import *
import enum


class MenuState(enum.Enum):
    MainState = 1
    StartGameState = 2
    LoadGFameState = 3


class MainMenuLayer(Layer):
    def __init__(self, surface: pygame.Surface):
        self.menuState: MenuState = MenuState.MainState

        self.surface: pygame.Surface = surface

        self.mainInterfaceContainer = Container(surface.get_rect())

        font = Loader.get_font("ALoveOfThunder.ttf", 200)

        title_label = Label(font.render("worms.py", True, (50, 30, 20)))
        title_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        title_label.constraintManager.add_height_constraint(AspectConstraint())
        title_label.constraintManager.add_x_constraint(CenterConstraint())
        title_label.constraintManager.add_y_constraint(RelativeMultConstraint(0.0))
        self.mainInterfaceContainer.add_element(title_label)

        start_game_button = Button(font.render("Start Game", True, (255, 0, 0)),
                                   font.render("Start Game", True, (255, 127, 0)))
        start_game_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.5))
        start_game_button.constraintManager.add_height_constraint(AspectConstraint())
        start_game_button.constraintManager.add_x_constraint(CenterConstraint())
        start_game_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.3))
        start_game_button.set_click_function(lambda _: self.change_state(MenuState.StartGameState))
        self.mainInterfaceContainer.add_element(start_game_button)

        load_game_button = Button(font.render("Load Game", True, (255, 0, 0)),
                                  font.render("Load Game", True, (255, 127, 0)))
        load_game_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.5))
        load_game_button.constraintManager.add_height_constraint(AspectConstraint())
        load_game_button.constraintManager.add_x_constraint(CenterConstraint())
        load_game_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.5))
        load_game_button.set_click_function(self.load_game)
        self.mainInterfaceContainer.add_element(load_game_button)

        exit_button = Button(font.render("Exit", True, (0, 255, 0)),
                             font.render("Exit", True, (0, 255, 127)))
        exit_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        exit_button.constraintManager.add_height_constraint(AspectConstraint())
        exit_button.constraintManager.add_x_constraint(CenterConstraint())
        exit_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.7))
        exit_button.set_click_function(self.exit_game)
        self.mainInterfaceContainer.add_element(exit_button)

        self.startGameContainer: Container = Container(surface.get_rect())
        self.startGameContainer.set_color(pygame.Color(255, 255, 255))

        title_label = Label(font.render("Start Game", True, (50, 30, 20)))
        title_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        title_label.constraintManager.add_height_constraint(AspectConstraint())
        title_label.constraintManager.add_x_constraint(CenterConstraint())
        title_label.constraintManager.add_y_constraint(RelativeMultConstraint(0.0))
        self.startGameContainer.add_element(title_label)

        first_level_button = Button(pygame.image.load("res/images/bbpreview.png"))
        first_level_button.constraintManager.add_x_constraint(RelativeAddConstraint(0.2))
        first_level_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.4))
        first_level_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        first_level_button.constraintManager.add_height_constraint(AspectConstraint())
        first_level_button.set_click_function(lambda e: self.start_game("data/levels/bikini_bottom.json"))
        self.startGameContainer.add_element(first_level_button)

        bb_label = Label(font.render("Bikini Bottom", True, (50, 30, 20)))
        bb_label.constraintManager.add_x_constraint(RelativeAddConstraint(0.2))
        bb_label.constraintManager.add_y_constraint(RelativeAddConstraint(0.6))
        bb_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        bb_label.constraintManager.add_height_constraint(AspectConstraint())
        self.startGameContainer.add_element(bb_label)
        self.startGameContainer.add_element(title_label)


    def on_attach(self):
        self.mainInterfaceContainer.set_all_visible()
        self.startGameContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        self._get_selected_container().on_update()

    def on_render(self):
        self.surface.fill((255, 0, 255))

        self._get_selected_container().on_render(self.surface)

    def on_event(self, event):
        self._get_selected_container().on_event(event)

    def change_state(self, state):
        self.menuState = state

    @staticmethod
    def start_game(level_path):
        from engine.application import Application
        Application.Instance.start_level(level_path)

    @staticmethod
    def load_game(_):
        print("Load game")

    @staticmethod
    def exit_game(_):
        from engine.application import Application
        Application.Instance.running = False

    def _get_selected_container(self):
        if self.menuState == MenuState.MainState:
            return self.mainInterfaceContainer
        elif self.menuState == MenuState.StartGameState:
            return self.startGameContainer
