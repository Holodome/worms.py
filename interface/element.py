import abc

from engine import Rect
from .constraint import ConstraintManager


class Element:
    _rect: Rect = Rect(0, 0, 1, 1)

    def __init__(self):
        self._visible: bool = False
        self.constraints = ConstraintManager()

    @abc.abstractmethod
    def on_update(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_render(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_event(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def apply_rect(self):
        raise NotImplementedError

    def set_visible(self, visible: bool):
        self._visible = visible
