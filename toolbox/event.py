import sys

import pygame


class Keyboard:
    """
    Class for storing keyboard input
    """

    def __init__(self):
        self.heldKeys: set = set()
        self.keysPressedThisFrame: set = set()
        self.keysReleasedThisFrame: set = set()

    def update(self):
        self.keysPressedThisFrame.clear()
        self.keysReleasedThisFrame.clear()

    def report_key_press(self, key):
        self.heldKeys.add(key)
        self.keysPressedThisFrame.add(key)

    def report_key_release(self, key):
        self.heldKeys.remove(key)
        self.keysReleasedThisFrame.add(key)

    def key_is_held(self, key):
        return key in self.heldKeys

    def key_is_pressed(self, key):
        return key in self.keysPressedThisFrame

    def key_is_released(self, key):
        return key in self.keysReleasedThisFrame


class Mouse:
    """
    Class for storing mouse input,
    movement and wheel scrolling
    """

    def __init__(self, screen_size: list):
        self.screenSize: list = screen_size

        self.heldButtons: set = set()
        self.buttonsPressedThisFrame: set = set()
        self.buttonsReleasedThisFrame: set = set()

        self.x = self.y = 0.0
        self.dx = self.dy = 0.0
        self._lastX = self._lastY = 0.0

    def update(self):
        self.buttonsPressedThisFrame.clear()
        self.buttonsReleasedThisFrame.clear()

        self.dx = self._lastX - self.x
        self.dy = self._lastY - self.y
        self._lastX = self.x
        self._lastY = self.y

    def report_button_press(self, button):
        self.heldButtons.add(button)
        self.buttonsPressedThisFrame.add(button)

    def report_button_release(self, button):
        self.heldButtons.remove(button)
        self.buttonsReleasedThisFrame.add(button)

    def button_is_held(self, button):
        return button in self.heldButtons

    def button_is_pressed(self, button):
        return button in self.buttonsPressedThisFrame

    def button_is_released(self, button):
        return button in self.buttonsReleasedThisFrame


class Input(Keyboard, Mouse):
    """
    This class controls all event - related things
    """

    def __init__(self, screen_size):
        Keyboard.__init__(self)
        Mouse.__init__(self, screen_size)

    def update(self):
        Keyboard.update(self)
        Mouse.update(self)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                self.report_key_press(event.key)
            elif event.type == pygame.KEYUP:
                self.report_key_release(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.report_button_press(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.report_button_release(event.button)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                self.x = mx / self.screenSize[0]
                self.y = my / self.screenSize[1]

            elif event.type == pygame.VIDEOEXPOSE:
                return True
        return False
