import pygame

from .button import Button


class Menu:
    def __init__(self, x: int, y: int, size: tuple, *args):
        self.x = x
        self.y = y

        self.size: tuple = size
        self.elements = list(args)

    def mouse_on(self, mouse_pos):
        for element in self.elements:
            if isinstance(element, Button):
                element.hovered = element.mouse_on(mouse_pos)

    def click(self, mouse_pos, *args):
        for element in self.elements:
            if isinstance(element, Button):
                if element.mouse_on(mouse_pos):
                    return element.click(*args)

    def draw(self, screen: pygame.Surface):
        for element in self.elements:
            element.draw(screen, self.position)

    @property
    def position(self):
        return self.x, self.y
