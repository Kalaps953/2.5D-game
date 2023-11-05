from classes.object import *
from config import *
import math
import pygame as pg


class Player:
    def __init__(self, pos: Pos, angle: float = 0, fov: int = 90, dov: int = 255, aol: int = 100, dof: float = 10):
        self._pos = pos
        # Угол камеры
        self._angle = angle
        # Поле зрения (field of view)
        self.fov = fov / 180 * math.pi
        # Кол-во линий (amount of lines)
        self.aol = aol
        # Дистанция отрисовки (distance of view)
        self.dov = dov
        self.dof = dof
        # Линии для трассировки, если можно так выразиться
        self.lines = self.get_lines()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.lines = self.get_lines()

    @pos.getter
    def pos(self):
        return self._pos

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.lines = self.get_lines()

    @angle.getter
    def angle(self):
        return self._angle

    def get_lines(self):
        lines = []
        for i in range(-self.aol // 2, self.aol // 2):
            st = self.fov / self.aol
            a = st * i
            c = math.cos(a)
            k = math.sin(a) / math.cos(a)
            lines.append(
                Line(self._pos + Pos(0, k * c * self.dof), Pos(math.cos(a) * self.dov, math.sin(a) * self.dov) + self._pos,
                     color=[0, 0, 255]))
            lines[-1] = lines[-1].get_rotated(self._angle, self._pos)
        return lines

    def draw_lines(self, display: pg.Surface):
        for i in self.lines:
            i.draw_on_map(display)

    def draw(self, display: pg.Surface, map):
        x = 0
        step = round(WIDTH / self.aol) + 1
        for i in self.lines:
            max_distance = i.get_distance()
            da = 255 / max_distance
            distances = []
            for j in map.lines:
                p = i.collide(j)
                if p is not False:
                    distances.append(Line(self.pos, p).get_distance())
                    if distances[-1] > max_distance:
                        distances[-1] = max_distance
                    if distances[-1] <= 0:
                        distances[-1] = 1
            if distances:
                distances.sort(reverse=True)
                for d in distances:
                    height = self.dof / d * (HEIGHT - self.dof)
                    clr = int(da * d)
                    pg.draw.rect(display, [clr, clr, clr], [x, (HEIGHT - height) / 2, step, height])
            x += step

    def move(self, map, vector: Pos):
        an = (vector + self._pos).get_angle(self._pos)

        check_l1 = Line(self._pos, self._pos + vector + Pos(math.cos(an) * self.dof * 1.42, math.sin(an) * self.dof * 1.42))
        check_l2 = Line(self._pos, self._pos + Pos(math.cos(an + math.pi / 4) * self.dof * 1.42, math.sin(an + math.pi / 4) * self.dof * 1.42))
        check_l3 = Line(self._pos, self._pos + Pos(math.cos(an - math.pi / 4) * self.dof * 1.42,
                                                   math.sin(an - math.pi / 4) * self.dof * 1.42))
        coll = False
        for i in map.lines:
            if i.collide(check_l1) or i.collide(check_l2) or i.collide(check_l3):
                coll = True
                break
        if coll:
            return
        self.pos += vector

