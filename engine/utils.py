from typing import Tuple

from .types import Vector2


def clamp(v, mi, ma):
    return min(ma, max(mi, v))


def vec_to_itup(vec: Vector2) -> Tuple[int, int]:
    return int(vec.x), int(vec.y)
