import pygame as pg


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_arr(self):
        return [self.x, self.y]

    def draw_on_map(self, display: pg.Surface, color):
        pg.draw.circle(display, color, self.get_arr(), 5)

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

