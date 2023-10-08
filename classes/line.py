from classes.object import Pos
import pygame as pg
import math


class Line:
    def __init__(self, pos1: Pos, pos2: Pos, id=1, color: list=[0, 0, 0]):
        self.start = pos1
        self.end = pos2
        self.color = color
        self.id = id

    def __str__(self):
        return f's= ({self.start});; e= ({self.end})'

    def get_distance(self):
        d = (self.start - self.end) ** 2
        return math.sqrt(d.x + d.y)

    def normalize(self):
        self.end -= self.start
        self.start -= self.start
        self.end /= self.get_distance()
        return self.end

    def draw_on_map(self, display: pg.Surface):
        pg.draw.line(display, self.color, self.start.get_arr(), self.end.get_arr())

    def collide(self, line, r=False):
        print(self.id)
        if self.start > line.start > self.end or self.start > line.end > self.end or \
                self.start < line.start < self.end or self.start < line.end < self.end:
            k = self.end - self.start
            k = Line(Pos(0, 0), k)
            k = k.end / k.get_distance()
            if k.x != 0:
                kx = k.y / k.x
                psx = Pos(line.start.x, kx * line.start.x)
                pex = Pos(line.end.x, kx * line.end.x)
            else:
                psx = Pos(line.start.x, self.start.y)
                pex = Pos(line.end.x, self.end.y)

            if k.y != 0:
                ky = k.x / k.y
                psy = Pos(ky * line.start.y, line.start.y)
                pey = Pos(ky * line.end.y, line.end.y)
            else:
                psy = Pos(self.start.x, line.start.y)
                pey = Pos(self.end.x, line.end.y)
            k = line.end - line.start
            k = Line(Pos(0, 0), k)
            k = k.normalize()
            if Line(self.start, psx).get_distance() <= self.get_distance() or Line(self.start, psy).get_distance() < self.get_distance():
                if (line.end.y >= psx.y >= line.start.y or line.start.y >= psx.y >= line.end.y) and \
                        (line.end.x >= psy.x >= line.start.x or line.start.x >= psy.x >= line.end.x):
                    return [True, Pos(psx.y * ky, psx.y), Pos(psy.x, psy.x * kx), Pos(psx.y * ky, psy.x * kx)]

            if Line(self.start, pex).get_distance() <= self.get_distance() or Line(self.start, pey).get_distance() < self.get_distance():
                if (line.end.y >= pex.y >= line.start.y or line.start.y >= pex.y >= line.end.y) and \
                        (line.end.x >= pey.x >= line.start.x or line.start.x >= pey.x >= line.end.x):
                    return [True, Pos(ky * pex.y, pex.y), Pos(pey.x, kx * pey.x), Pos(pex.y * ky, pey.x * kx)]

        if not r:
            return line.collide(self, r=True)
        return False
