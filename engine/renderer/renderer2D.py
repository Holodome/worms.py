from typing import List, Tuple

import pygame

from .camera import Camera
from engine.window import Window


class Renderer2D:
    entities: List[Tuple[pygame.Surface, pygame.Vector2]] = []
    cameraTranslation: Tuple[int, int] = (0, 0)
    windowRect: pygame.Rect = pygame.Rect(0, 0, 1, 1)
    windowSurface: pygame.Surface = None

    @staticmethod
    def begin_scene(camera: Camera):
        Renderer2D.entities.clear()
        Renderer2D.cameraTranslation = tuple(map(int, -camera.get_position()))
        wi = Window.Instance
        Renderer2D.windowSurface = wi.get_surface()
        Renderer2D.windowRect = pygame.Rect(0, 0, wi.width, wi.height)

    @staticmethod
    def submit(entity):
        tp = entity.position + Renderer2D.cameraTranslation
        tr = pygame.Rect(tp, entity.image.get_size())
        if Renderer2D.windowRect.colliderect(tr):
            Renderer2D.entities.append((entity.image, tp))

    @staticmethod
    def present():
        Renderer2D.windowSurface.blit(* Renderer2D.entities[0])
        Renderer2D.windowSurface.blits(Renderer2D.entities, doreturn=False)
