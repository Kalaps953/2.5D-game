from classes.object import *
from config import *
import math
import pygame as pg


class Camera:
    def __init__(self, pos: Pos, angle: float=0, fov: int=90, dov: int = 500, aol: int = 500):
        self._pos = pos
        # Угол камеры
        self._angle = angle
        # Поле зрения (field of view)
        self.fov = fov / 360 * math.pi
        # Кол-во линий (amount of lines)
        self.aol = aol
        # Дистанция отрисовки (distance of view)
        self.dov = dov
        # Линии для трассировки, если можно так выразиться
        self.lines = []
        for i in range(-(self.aol // 2), self.aol // 2):
            self.lines.append(Line(self.pos, Pos(math.cos(i * (self.fov / self.aol) + self.angle) * self.dov, math.sin(i * (self.fov / self.aol) + self.angle) * self.dov)))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        for i in self.lines:
            i += self._pos - value
        self._pos = value

    @pos.getter
    def pos(self):
        return self._pos

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.lines = []
        for i in range(-(self.aol // 2), self.aol // 2):
            self.lines.append(Line(self.pos, Pos(math.cos(i * (self.fov / self.aol) + self.angle) * self.dov, math.sin(i * (self.fov / self.aol) + self.angle) * self.dov)))

    @angle.getter
    def angle(self):
        return self._angle

    def draw(self, display: pg.Surface, map):
        x = 0
        step = WIDTH / self.aol
        he = HEIGHT / self.dov
        for i in self.lines:
            for j in map.lines:
                p = i.collide(j)
                if p:
                    d = Line(self.pos, p).get_distance()
                    pg.draw.rect(display, [0, 0, 0], [x, he * d // 2, x + step, HEIGHT - he * d // 2])
            x += step
