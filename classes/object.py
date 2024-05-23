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
        d = l.get_distance()
        if d > 0:
            n = (l.end.y - l.start.y) / l.get_distance()
        else:
            n = 0
        angle = math.asin(n)
        if l.end.x - l.start.x < 0:
            return math.pi / 2 - angle + math.pi / 2
        return angle

    def get_rotated_on(self, angle: float, pos):
        angle = self.get_angle(pos) + angle
        d = Line(pos, self).get_distance()
        return pos + Pos(math.cos(angle) * d, math.sin(angle) * d)

    def get_rotated_to(self, angle: float, pos):
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
            return Pos(math.pow(self.x,  power), math.pow(self.y, power))
        if isinstance(power, int):
            return Pos(math.pow(self.x,  power), math.pow(self.y, power))
        elif isinstance(power, Pos):
            return Pos(math.pow(self.x, power.x), math.pow(self.y, power.y))

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
    def __init__(self, pos1: Pos, pos2: Pos, id=1, color: list = [0, 0, 0]):
        self.start = pos1
        self.end = pos2
        self.color = color
        self.id = id
        self.A = self.end.y - self.start.y
        self.B = self.end.x - self.start.x
        self.C = self.end.x * self.start.y - self.start.x * self.end.y

    def __str__(self):
        return f's= ({self.start});; e= ({self.end});'

    def get_distance(self):
        dx = self.start.x - self.end.x
        dx = math.pow(dx, 2)
        dy = self.start.y - self.end.y
        dy = math.pow(dy, 2)
        return math.sqrt(dx + dy)

    def get_normalized(self):
        d = self.get_distance()
        if d != 0:
            return (self.end - self.start) / d
        return Pos(0, 0)

    def draw_on_map(self, display: pg.Surface):
        pg.draw.line(display, self.color, self.start.get_arr(), self.end.get_arr())

    def __add__(self, other):
        if isinstance(other, Pos):
            return Line(self.start + other, self.end + other, self.id, self.color)

    def __sub__(self, other):
        if isinstance(other, Pos):
            return Line(self.start - other, self.end - other, self.id, self.color)

    def collide(self, l):
        assert isinstance(l, Line), 'Line.check_collide needs only input as Line'
        n = l.A * self.B - self.A * l.B
        if n != 0:
            p = Pos((l.B * self.C - self.B * l.C) / n, (l.A * self.C - self.A * l.C) / n)

            def ch(v, v1, v2):
                if v1 < v2:
                    if v1 <= v <= v2:
                        return True
                    return False
                elif v1 > v2:
                    if v1 >= v >= v2:
                        return True
                    return False
                else:
                    return True
            if ch(p.x, self.start.x, self.end.x) and ch(p.x, l.start.x, l.end.x):
                if ch(p.y, self.start.y, self.end.y) and ch(p.y, l.start.y, l.end.y):
                    return p
        return False

    def get_rotated_on(self, angle: float, pos: Pos):
        return Line(self.start.get_rotated_on(angle, pos),
                    self.end.get_rotated_on(angle, pos), id=self.id, color=self.color)

    def get_rotated_to(self, angle: float, pos: Pos):
        return Line(self.start.get_rotated_to(angle, pos), self.end.get_rotated_to(angle, pos))
