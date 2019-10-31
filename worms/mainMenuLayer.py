import enum

from engine import *
from interface import *


class MenuState(enum.Enum):
    MainState = 1
    StartGameState = 2
    LoadGFameState = 3


class _MainInterfaceContainer(Container):
    def __init__(self):
        super().__init__(Rect(0, 0, Window.Instance.width, Window.Instance.height))

        font = Loader.get_font("ALoveOfThunder.ttf", 200)

        self.title_label = Label(font.render("worms.py", True, (50, 30, 20)))
        self.title_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        self.title_label.constraintManager.add_height_constraint(AspectConstraint())
        self.title_label.constraintManager.add_x_constraint(CenterConstraint())
        self.title_label.constraintManager.add_y_constraint(RelativeMultConstraint(0.0))
        self.add_element(self.title_label)

        self.start_game_button = Button(font.render("Start Game", True, (255, 0, 0)),
                                        font.render("Start Game", True, (255, 127, 0)))
        self.start_game_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.5))
        self.start_game_button.constraintManager.add_height_constraint(AspectConstraint())
        self.start_game_button.constraintManager.add_x_constraint(CenterConstraint())
        self.start_game_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.3))
        self.add_element(self.start_game_button)

        self.load_game_button = Button(font.render("Load Game", True, (255, 0, 0)),
                                       font.render("Load Game", True, (255, 127, 0)))
        self.load_game_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.5))
        self.load_game_button.constraintManager.add_height_constraint(AspectConstraint())
        self.load_game_button.constraintManager.add_x_constraint(CenterConstraint())
        self.load_game_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.5))
        self.add_element(self.load_game_button)

        self.exit_button = Button(font.render("Exit", True, (0, 255, 0)),
                                  font.render("Exit", True, (0, 255, 127)))
        self.exit_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        self.exit_button.constraintManager.add_height_constraint(AspectConstraint())
        self.constraint = self.exit_button.constraintManager.add_x_constraint(CenterConstraint())
        self.exit_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.7))
        self.add_element(self.exit_button)


class _StartGameContainer(Container):
    def __init__(self):
        super().__init__(Rect(0, 0, Window.Instance.width, Window.Instance.height))
        self.set_color(Color(255, 255, 255))

        font = Loader.get_font("ALoveOfThunder.ttf", 200)

        self.title_label = Label(font.render("Start Game", True, (50, 30, 20)))
        self.title_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.7))
        self.title_label.constraintManager.add_height_constraint(AspectConstraint())
        self.title_label.constraintManager.add_x_constraint(CenterConstraint())
        self.title_label.constraintManager.add_y_constraint(RelativeMultConstraint(0.0))
        self.add_element(self.title_label)

        self.first_level_button = Button(Loader.load_image("bbpreview"))
        self.first_level_button.constraintManager.add_x_constraint(RelativeAddConstraint(0.2))
        self.first_level_button.constraintManager.add_y_constraint(RelativeAddConstraint(0.4))
        self.first_level_button.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        self.first_level_button.constraintManager.add_height_constraint(AspectConstraint())
        self.add_element(self.first_level_button)

        self.bb_label = Label(font.render("Bikini Bottom", True, (50, 30, 20)))
        self.bb_label.constraintManager.add_x_constraint(RelativeAddConstraint(0.2))
        self.bb_label.constraintManager.add_y_constraint(RelativeAddConstraint(0.6))
        self.bb_label.constraintManager.add_width_constraint(RelativeMultConstraint(0.2))
        self.bb_label.constraintManager.add_height_constraint(AspectConstraint())
        self.add_element(self.bb_label)
        self.add_element(self.title_label)


class MainMenuLayer(Layer):
    def __init__(self):
        self.menuState: MenuState = MenuState.MainState
        # Создание контейнеров
        self.mainInterfaceContainer = _MainInterfaceContainer()
        self.startGameContainer = _StartGameContainer()
        # Привязка кнопок к функциям
        self.mainInterfaceContainer.start_game_button.set_click_function(
            lambda _: self.change_state(MenuState.StartGameState))
        self.mainInterfaceContainer.load_game_button.set_click_function(self.load_game)
        self.mainInterfaceContainer.exit_button.set_click_function(self.exit_game)

        self.startGameContainer.first_level_button.set_click_function(
            lambda _: self.start_game("data/levels/bikini_bottom.json"))

    def on_attach(self):
        self.mainInterfaceContainer.set_all_visible()
        self.startGameContainer.set_all_visible()

    def on_detach(self):
        pass

    def on_update(self, timestep):
        self._get_selected_container().on_update()

    def on_render(self):
        Renderer2D.begin_scene()
        Renderer2D.RendererCommand.clear_screen(255, 255, 255)
        self._get_selected_container().on_render()

    def on_event(self, dispatcher):
        self._get_selected_container().on_event(dispatcher)

        dispatcher.dispatch(plocals.VIDEORESIZE, lambda e: [
            self.mainInterfaceContainer.set_rect(Rect(0, 0, e.w, e.h))
        ])

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
