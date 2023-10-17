from classes.line import *
from classes.object import *
from config import *
import math
import pygame as pg


class Camera:
    def __init__(self, pos: Pos, angle: float=0, fov: int=90, dov: int = 500):
        self._pos = pos
        # Угол камеры
        self._angle = angle / 360 * math.pi
        # Поле зрения (field of view)
        self.fov = fov / 360 * math.pi
        # Кол-во линий (amount of lines)
        self.aol = WIDTH
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

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.lines = []
        for i in range(-(self.aol // 2), self.aol // 2):
            self.lines.append(Line(self.pos, Pos(math.cos(i * (self.fov / self.aol) + self.angle) * self.dov, math.sin(i * (self.fov / self.aol) + self.angle) * self.dov)))

    def draw(self, display: pg.Surface):
        for i in self.lines:
            pass
