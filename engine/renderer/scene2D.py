from typing import List

from .camera import Camera
from .entity import Entity
from .renderer2D import Renderer2D


class Scene2D:
    def __init__(self, camera: Camera):
        self.entities: List[Entity] = []
        self.camera: Camera = camera

    def on_update(self) -> None:
        self.entities = list(filter(lambda e: e.Alive, self.entities))

    def add(self, entity: Entity) -> None:
        self.entities.append(entity)

    def on_render(self) -> None:
        Renderer2D.begin_scene(self.camera.negative_translation)
        for entity in self.entities:
            Renderer2D.submit(entity)
        Renderer2D.present()
