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
        def blend_screen(r, g, b, a):
            surf = pygame.Surface(Renderer2D.windowRect.size)
            surf.fill((r, g, b, a))
            Renderer2D.windowSurface.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    @staticmethod
    def submit_one(entity: Union[Entity, Tuple[pygame.Surface, Tuple[int, int]]]):
        if isinstance(entity, Entity):
            Window.get_surface().blit(entity.image, entity.pos)
        else:
            Window.get_surface().blit(entity[0], entity[1])

    @staticmethod
    def begin_scene(camera_position: Tuple[int, int] = None):
        Renderer2D.entities.clear()
        if camera_position is not None:
            Renderer2D.cameraTranslation = camera_position
        Renderer2D.windowSurface = Window.get_surface()
        Renderer2D.windowRect = pygame.Rect(0, 0, Renderer2D.windowSurface.get_width(),
                                            Renderer2D.windowSurface.get_height())

    @staticmethod
    def submit(entity: Union[Entity, Tuple[pygame.Surface, Tuple[int, int]]], camera_affect: bool = True):

        if isinstance(entity, Entity):
            ent_pos = tuple(entity.pos)
            ent_img = entity.image
        else:
            ent_pos = entity[1]
            ent_img = entity[0]

        if camera_affect:
            tp = (int(ent_pos[0] + Renderer2D.cameraTranslation[0]),
                  int(ent_pos[1] + Renderer2D.cameraTranslation[1]))
            tr = pygame.Rect(tp, ent_img.get_size())
            if Renderer2D.windowRect.colliderect(tr):
                Renderer2D.entities.append((ent_img, tp))
        else:
            tr = pygame.Rect(ent_pos, ent_img.get_size())
            if Renderer2D.windowRect.colliderect(tr):
                Renderer2D.entities.append((ent_img, ent_pos))

    @staticmethod
    def present():
        Renderer2D.windowSurface.blits(Renderer2D.entities, doreturn=False)