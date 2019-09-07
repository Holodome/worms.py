import pygame


class Button:
    def __init__(self, static_image: pygame.Surface,
                 x: int, y: int, hover_image: pygame.Surface = None, click_func=None,
                 width: int = None,
                 height: int = None,
                 hover_width: int = None, hover_height: int = None):
        self.staticImage: pygame.Surface = static_image
        if hover_image is None:
            self.hoverImage: pygame.Surface = static_image
        else:
            self.hoverImage = hover_image

        self.staticRect = pygame.Rect(x, y, width if width is not None else static_image.get_width(),
                                      height if height is not None else static_image.get_height())

        if hover_image is not None:
            # TODO: reformat code
            self.hoverRect = pygame.Rect(x + self.staticRect.width / 2 - self.hoverImage.get_width() / 2,
                                         y + self.staticRect.height / 2 - self.hoverImage.get_height() / 2,
                                         hover_width if hover_width is not None else hover_image.get_width()
                                         if hover_image is not None else self.staticRect.width,
                                         hover_height if hover_height is not None else hover_image.get_height()
                                         if hover_image is not None else self.staticRect.height)
        else:
            self.hoverRect = self.staticRect
        self.hovered: bool = False

        self.click_func = click_func
        if click_func is None:
            self.click_func = lambda *args: args  # pass

    def mouse_on(self, mouse_pos: tuple) -> bool:
        collide = self.staticRect.collidepoint(*mouse_pos)
        self.hovered = collide
        return collide

    def click(self, *args):
        return self.click_func(*args)

    def draw(self, screen: pygame.Surface, offset):
        print(self.hovered)
        if self.hovered:
            screen.blit(self.hoverImage, self.hoverRect)
        else:
            screen.blit(self.staticImage, self.staticRect)
