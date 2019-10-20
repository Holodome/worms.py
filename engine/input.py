from typing import Tuple

import pygame


class Input:
    mouse_position = (0, 0)
    pressed_buttons = {}
    pressed_keys = {}

    @staticmethod
    def update() -> None:
        Input.mouse_position = pygame.mouse.get_pos()
        Input.pressed_buttons = pygame.mouse.get_pressed()
        Input.pressed_keys = pygame.key.get_pressed()

    @staticmethod
    def is_key_pressed(key) -> bool:
        return Input.pressed_keys.get(key, False)

    @staticmethod
    def is_button_pressed(btn) -> bool:
        return Input.pressed_buttons.get(btn, False)

    @staticmethod
    def get_mouse_pos() -> Tuple[int, int]:
        return Input.mouse_position
