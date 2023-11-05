import pygame as pg
import math


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_arr(self):
        return [int(self.x), int(self.y)]

    def draw(self, display: pg.Surface, color):
        pg.draw.circle(display, color, self.get_arr(), 2)

    def get_angle(self, pos):
        l = Line(pos, self)
        l = l.get_normalized()
        angle = math.asin(l.y)
        if l.x < 0:
            return math.pi / 2 - angle + math.pi / 2
        return angle

    def get_rotated(self, angle: float, pos):
        angle = self.get_angle(pos) + angle
        d = Line(pos, self).get_distance()
        return pos + Pos(math.cos(angle) * d, math.sin(angle) * d)

    def __str__(self):
        return f'x={self.x}; y={self.y}'

    # +
    def __add__(self, other):
        if isinstance(other, Pos):
            return Pos(self.x + other.x, self.y + other.y)

    # -
    def __sub__(self, other):
        if isinstance(other, Pos):
            return Pos(self.x - other.x, self.y - other.y)

    # /
    def __truediv__(self, other):
        if isinstance(other, float):
            return Pos(self.x / other, self.y / other)

    # **
    def __pow__(self, power, modulo=None):
        if isinstance(power, float):
            return Pos(self.x ** power, self.y ** power)
        if isinstance(power, int):
            return Pos(self.x ** power, self.y ** power)
        elif isinstance(power, Pos):
            return Pos(self.x ** power.x, self.y ** power.y)

    # <
    def __lt__(self, other):
        if isinstance(other, Pos):
            return self.x <= other.x or self.y <= other.y
        elif isinstance(other, float):
            return self.x <= other or self.y <= other

    # >
    def __gt__(self, other):
        if isinstance(other, Pos):
            return self.x >= other.x or self.y > other.y
        elif isinstance(other, float):
            return self.x >= other or self.y > other

    # <=
    def __le__(self, other):
        if isinstance(other, Pos):
            return self.x <= other.x and self.y <= other.y
        elif isinstance(other, float):
            return self.x <= other and self.y <= other

    # >=
    def __ge__(self, other):
        if isinstance(other, Pos):
            return self.x >= other.x and self.y >= other.y
        elif isinstance(other, float):
            return self.x >= other and self.y >= other


class Line:
    def __init__(self, pos1: Pos, pos2: Pos, id = 1, color: list = [0, 0, 0]):
        self.start = pos1
        self.end = pos2
        self.color = color
        self.id = id

    def __str__(self):
        return f's= ({self.start});; e= ({self.end});'

    def get_distance(self):
        d = (self.start - self.end) ** 2
        return math.sqrt(d.x + d.y)

    def get_normalized(self):
        d = self.get_distance()
        if d != 0:
            return (self.end - self.start) / self.get_distance()
        return Pos(0, 0)

    def draw_on_map(self, display: pg.Surface):
        pg.draw.line(display, self.color, self.start.get_arr(), self.end.get_arr())

    def __add__(self, other):
        if isinstance(other, Pos):
            return Line(self.start + other, self.end + other, self.id, self.color)

    def __sub__(self, other):
        if isinstance(other, Pos):
            return Line(self.start - other, self.end - other, self.id, self.color)

    def collide(self, line, r=True):
        if line.start < self.start < line.end or line.end < self.start < line.start or line.start < self.end < line.end or line.end < self.end < line.start:
            angle = self.end.get_angle(self.start)
            l1 = self.get_rotated(-angle, self.start)
            li = line.get_rotated(-angle, self.start)
            norm = li.get_normalized()
            if norm.y != 0:
                k = (l1.start.y - li.start.y) * (norm.x / norm.y) + li.start.x
            else:
                k = l1.start.y
            if (li.start.y <= l1.start.y <= li.end.y or li.end.y <= l1.start.y <= li.start.y) and (l1.start.x >= k >= l1.end.x or l1.end.x >= k >= l1.start.x):
                return Pos(k, l1.start.y).get_rotated(angle, self.start)
        if r:
            return line.collide(self, False)
        return False

    def get_rotated(self, angle: float, pos: Pos):
        return Line(self.start.get_rotated(angle, pos),
                    self.end.get_rotated(angle, pos), id=self.id, color=self.color)
