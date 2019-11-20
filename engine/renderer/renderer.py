from typing import List, Tuple, Union

import pygame

from .entity import Entity
from ..types import Rect
from ..window import Window


class Renderer:
    entities: List[Tuple[pygame.Surface, Tuple[int, int]]] = []
    cameraTranslation: Tuple[int, int] = (0, 0)
    windowSurface: pygame.Surface = None

    class Command:
        @staticmethod
        def clear_screen(r, g, b):
            Renderer.windowSurface.fill((r, g, b))

        @staticmethod
        def blend_screen(r, g, b, a):
            surf = pygame.Surface(Renderer.windowSurface.get_size())
            surf.fill((r, g, b, a))
            Renderer.windowSurface.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    @staticmethod
    def start_frame():
        Renderer.entities.clear()

    @staticmethod
    def begin_scene(camera_position: Tuple[int, int] = None):
        if camera_position is not None:
            Renderer.cameraTranslation = camera_position
        Renderer.windowSurface = Window.get_surface()
        Renderer.windowRect = Rect(0, 0, Renderer.windowSurface.get_width(),
                                   Renderer.windowSurface.get_height())

    @staticmethod
    def submit(entity: Union[Entity, Tuple[pygame.Surface, Tuple[int, int]]], camera_affect: bool = True):
        if isinstance(entity, Entity):
            ent_pos = tuple(entity.pos)
            ent_img = entity.image
        else:
            ent_pos = entity[1]
            ent_img = entity[0]

        if camera_affect:
            tp = (int(ent_pos[0] + Renderer.cameraTranslation[0]),
                  int(ent_pos[1] + Renderer.cameraTranslation[1]))
            # Проверки на пересечение с экраном замедляют
            # tr = Rect(tp, ent_img.get_size())
            # if Renderer2D.windowRect.colliderect(tr):
            Renderer.entities.append((ent_img, tp))
        else:
            # tr = Rect(ent_pos, ent_img.get_size())
            # if Renderer2D.windowRect.colliderect(tr):
            Renderer.entities.append((ent_img, ent_pos))

    @staticmethod
    def present():
        Renderer.windowSurface.blits(Renderer.entities, doreturn=False)
