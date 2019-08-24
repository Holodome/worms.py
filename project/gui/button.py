import pygame


class Button:
    def __init__(self, static_image: pygame.Surface, hover_image: pygame.Surface,
                 x: int, y: int, width: int = None, height: int = None):
        self.staticImage: pygame.Surface = static_image
        self.hoverImage: pygame.Surface = hover_image

        if width is None:
            width = static_image.get_width()
        if height is None:
            height = static_image.get_height()

        self.rect = pygame.Rect(x, y, width, height)

        self.hovered: bool = False

    def mouse_on(self, mouse_pos: tuple) -> bool:
        collide = self.rect.collidepoint(*mouse_pos)
        self.hovered = collide
        return collide

    def draw(self, screen: pygame.Surface):
        if self.hovered:
            screen.blit(self.hoverImage, self.rect)
        else:
            screen.blit(self.staticImage, self.rect)
