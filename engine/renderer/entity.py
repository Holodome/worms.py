import pygame


class Entity:
    def __init__(self, image: pygame.Surface, position: pygame.Vector2):
        self.image = image
        self.position = position
