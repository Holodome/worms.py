from typing import Tuple

import pygame


class Input:
    mouse_position = (0, 0)
    _pressed_buttons: Tuple[bool, bool, bool] = (0, 0, 0)
    _pressed_keys: pygame.key.ScancodeWrapper = None

    @staticmethod
    def update() -> None:
        Input.mouse_position = pygame.mouse.get_pos()
        Input._pressed_buttons = pygame.mouse.get_pressed()
        Input._pressed_keys = pygame.key.get_pressed()

    @staticmethod
    def is_key_pressed(key: int) -> bool:
        return Input._pressed_keys[key]

    @staticmethod
    def is_button_pressed(btn: int) -> bool:
        return Input._pressed_buttons[btn]

    @staticmethod
    def get_mouse_pos() -> Tuple[int, int]:
        return Input.mouse_position
