from line import *
from camera import *
from object import *
import pygame as pg


class Map:
    def __init__(self, lines: list(Line), camera):
        self.lines = lines
        self.camera = camera

    # Повернуть все относительно точки отсчета (rotate all from starting point)
    def rafsp(self, angle):
        angles = []
        for i in self.lines:
            angles.append([i.start / Line(Pos(0, 0), i.start).get_distance(), Line(Pos(0, 0), i.start).get_distance()])
            angles[-1][0] = math.atan(angles[-1][0].y / angles[-1][0].x)
        for i in angles:
            i[0] += angle
        new_lines = []
        for i in range(len(angles)):
            d_e = self.lines[i].get_distance()
            a_e = math.atan(self.lines[i].get_normalized().y / self.lines[i].get_normalized().x) + angle
            a_s = angles[i][0]
            d_s = angles[i][1]
            p_s = Pos(math.cos(a_s) * d_s, math.sin(a_s) * d_s)
            new_lines.append(Line(p_s, p_s + Pos(math.cos(a_e) * d_e, math.sin(a_e) * d_e)))
