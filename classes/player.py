from classes.object import *
from config import *
import math
import pygame as pg


class Player:
    def __init__(self, pos: Pos, angle: float=0, fov: int=90, dov: int = 500, aol: int = 100):
        self._pos = pos
        # Угол камеры
        self._angle = angle
        # Поле зрения (field of view)
        self.fov = fov / 180 * math.pi
        # Кол-во линий (amount of lines)
        self.aol = aol
        # Дистанция отрисовки (distance of view)
        self.dov = dov
        # Линии для трассировки, если можно так выразиться
        self.lines = []
        for i in range(-self.aol // 2, self.aol // 2):
            st = self.fov / self.aol
            a = st * i + self.angle
            self.lines.append(Line(self.pos, Pos(round(math.cos(a) * self.dov), round(math.sin(a) * self.dov)) + self._pos, color=[0, 0, 255]))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.lines = []
        for i in range(-self.aol // 2, self.aol // 2):
            st = self.fov / self.aol
            a = st * i + self.angle
            self.lines.append(Line(self.pos, Pos(round(math.cos(a) * self.dov), round(math.sin(a) * self.dov)) + self._pos, color=[0, 0, 255]))

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
        for i in range(-self.aol // 2, self.aol // 2):
            st = self.fov / self.aol
            a = st * i + self.angle
            self.lines.append(Line(self.pos, Pos(round(math.cos(a) * self.dov), round(math.sin(a) * self.dov)) + self._pos, color=[0, 0, 255]))

    @angle.getter
    def angle(self):
        return self._angle

    def draw_lines(self, display: pg.Surface):
        for i in self.lines:
            i.draw_on_map(display)

    def draw(self, display: pg.Surface, map):
        x = 0
        step = WIDTH / self.aol
        he = HEIGHT / self.dov
        for i in self.lines:
            for j in map.lines:
                p = i.collide(j)
                if p is not False:
                    d = Line(self.pos, p).get_distance()
                    pg.draw.rect(display, [0, 0, 0], [x, he * d // 2, step, HEIGHT - he * d])
                    p.draw(display, [0, 255, 0])
            x += step
