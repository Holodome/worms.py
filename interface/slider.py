from engine import Input, Rect, plocals
from .element import Element

BUTTON_WIDTH = 10
MAX_VALUE = 100


class Slider(Element):
    def __init__(self, value: int, horizontal: bool = True):
        Element.__init__(self)
        self.horizontal: bool = horizontal

        self.currentValue = value
        self.buttonRect = Rect()

        self.currentlySliding: bool = False

    def _change_button_rect(self):
        if self.horizontal:
            self.buttonRect.x = (self.currentValue / MAX_VALUE) * self._rect.w + self._rect.x
            self.buttonRect.y = self._rect.y
            self.buttonRect.w = BUTTON_WIDTH
            self.buttonRect.h = self._rect.h
        else:
            self.buttonRect.x = self._rect.x
            self.buttonRect.y = (self.currentValue / MAX_VALUE) * self._rect.h + self._rect.y
            self.buttonRect.w = self._rect.w
            self.buttonRect.h = BUTTON_WIDTH

    def on_update(self):
        mx, my = Input.get_mouse_pos()
        if not self.currentlySliding:
            self.currentlySliding = self.buttonRect.collidepoint(mx, my)

        if self.currentlySliding:
            if self.horizontal:
                self.currentValue = (mx - self._rect.x) / self._rect.w
            else:
                self.currentValue = (my - self._rect.y) / self._rect.h

    def on_render(self):
        pass

    def on_event(self, event):
        event.dispatch(plocals.MOUSEBUTTONUP, setattr(self, "currentlySliding", False))

    def apply_rect(self):
        self._change_button_rect()

