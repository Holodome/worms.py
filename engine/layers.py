import abc
from typing import *


class Layer:
    @abc.abstractmethod
    def on_attach(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_detach(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_update(self, timestep):
        raise NotImplementedError

    @abc.abstractmethod
    def on_render(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_event(self, event):
        raise NotImplementedError


class LayerStack:

    def __init__(self):
        self.layers: List[Layer] = []
        self.layerInsertIndex = 0

    def __iter__(self) -> Iterable[Layer]:
        return iter(reversed(self.layers))

    def push_layer(self, layer: Layer):
        self.layers.insert(self.layerInsertIndex, layer)
        self.layerInsertIndex += 1
        layer.on_attach()

    def push_overlay(self, layer: Layer):
        self.layers.append(layer)
        layer.on_attach()

    def pop_layer(self, layer: Layer):
        ind = self.layers.index(layer, 0, self.layerInsertIndex)
        layer.on_detach()
        del self.layers[ind]
        self.layerInsertIndex -= 1

    def pop_overlay(self, layer: Layer):
        ind = self.layers.index(layer, self.layerInsertIndex, len(self.layers))
        layer.on_detach()
        del self.layers[ind]
