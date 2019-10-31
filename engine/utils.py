import dataclasses
from typing import Tuple


def clamp(v, mi, ma):
    return min(ma, max(mi, v))

