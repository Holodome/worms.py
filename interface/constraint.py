import abc
import enum

from engine import Rect


class ConstraintType(enum.Enum):
    Null = 0

    ConstraintX = 1
    ConstraintY = 2
    ConstraintWidth = 3
    ConstraintHeight = 4


class Constraint:
    constraintType = ConstraintType.Null

    def set_type(self, ct: ConstraintType):
        self.constraintType: ConstraintType = ct
        return self

    @abc.abstractmethod
    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        raise NotImplementedError


class RelativeMultConstraint(Constraint):

    def __init__(self, value: float):
        self.value: float = value

    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        if self.constraintType == ConstraintType.ConstraintX:
            target_rect.x = source_rect.x * self.value
        if self.constraintType == ConstraintType.ConstraintY:
            target_rect.y = source_rect.y * self.value
        if self.constraintType == ConstraintType.ConstraintWidth:
            target_rect.w = source_rect.w * self.value
        if self.constraintType == ConstraintType.ConstraintHeight:
            target_rect.h = source_rect.h * self.value


class RelativeAddConstraint(Constraint):

    def __init__(self, value: float):
        self.value: float = value

    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        if self.constraintType == ConstraintType.ConstraintX:
            target_rect.x = source_rect.x + self.value * source_rect.w
        if self.constraintType == ConstraintType.ConstraintY:
            target_rect.y = source_rect.y + self.value * source_rect.h


class AbsoluteAddConstraint(Constraint):
    def __init__(self, value: float):
        self.value: float = value

    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        if self.constraintType == ConstraintType.ConstraintX:
            target_rect.x = source_rect.x + self.value
        if self.constraintType == ConstraintType.ConstraintY:
            target_rect.y = source_rect.y + self.value


class AspectConstraint(Constraint):
    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        if self.constraintType == ConstraintType.ConstraintWidth:
            target_rect.w = target_rect.h / initial_rect.h * initial_rect.w
        elif self.constraintType == ConstraintType.ConstraintHeight:
            target_rect.h = target_rect.w / initial_rect.w * initial_rect.h


class CenterConstraint(Constraint):
    def update_value(self, source_rect: Rect, target_rect: Rect, initial_rect: Rect):
        if self.constraintType == ConstraintType.ConstraintX:
            target_rect.x = (source_rect.w - target_rect.w) / 2
        if self.constraintType == ConstraintType.ConstraintY:
            target_rect.y = (source_rect.h - target_rect.h) / 2


class ConstraintManager:
    def __init__(self):
        self.constraints = []

    def update_rect(self, rect: Rect, target_rect: Rect):
        initial_rect = target_rect.copy()
        for constraint in self.constraints:
            constraint.update_value(rect, target_rect, initial_rect)

    def add_x_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
        constraint.set_type(ConstraintType.ConstraintX)

    def add_y_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
        constraint.set_type(ConstraintType.ConstraintY)

    def add_width_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
        constraint.set_type(ConstraintType.ConstraintWidth)

    def add_height_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
        constraint.set_type(ConstraintType.ConstraintHeight)
