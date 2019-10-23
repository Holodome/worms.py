from typing import List, Tuple, Union

import pygame

from engine.window import Window
from .entity import Entity


class Renderer2D:
    entities: List[Tuple[pygame.Surface, Union[pygame.Vector2, Tuple[int, int]]]] = []
    cameraTranslation: Tuple[int, int] = (0, 0)
    windowRect: pygame.Rect = pygame.Rect(0, 0, 1, 1)
    windowSurface: pygame.Surface = None

    class RendererCommand:
        @staticmethod
        def clear_screen(r, g, b):
            Renderer2D.windowSurface.fill((r, g, b))

    @staticmethod
    def submit_one(entity: Union[Entity, Tuple[pygame.Surface, Tuple[int, int]]]):
        if isinstance(entity, Entity):
            Window.get_surface().blit(entity.image, entity.position)
        else:
            Window.get_surface().blit(entity[0], entity[1])

    @staticmethod
    def begin_scene(camera_position: Tuple[int, int]):
        Renderer2D.entities.clear()
        Renderer2D.cameraTranslation = camera_position
        Renderer2D.windowSurface = Window.get_surface()
        Renderer2D.windowRect = pygame.Rect(0, 0, Renderer2D.windowSurface.get_width(),
                                            Renderer2D.windowSurface.get_height())

    @staticmethod
    def submit(entity: Entity, camera_affect: bool = True):
        if camera_affect:
            tp = (int(entity.position.x + Renderer2D.cameraTranslation[0]),
                  int(entity.position.y + Renderer2D.cameraTranslation[1]))
            tr = pygame.Rect(tp, entity.image.get_size())
            if Renderer2D.windowRect.colliderect(tr):
                Renderer2D.entities.append((entity.image, tp))
        else:
            tr = pygame.Rect(entity.position, entity.image.get_size())
            if Renderer2D.windowRect.colliderect(tr):
                Renderer2D.entities.append((entity.image, entity.position))

    @staticmethod
    def present():
        Renderer2D.windowSurface.blits(Renderer2D.entities, doreturn=False)
