from classes.line import *
from classes.camera import *
from classes.object import *
import pygame as pg


class Map:
    def __init__(self, lines: list, camera):
        self.lines = lines
        self.camera = camera

    # Повернуть все относительно точки отсчета (rotate all from starting point)
    def rafsp(self, angle: float):
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
            print(d_s)
            p_s = Pos(math.cos(a_s) * d_s, math.sin(a_s) * d_s)
            new_lines.append(Line(p_s, p_s + Pos(math.cos(a_e) * d_e, math.sin(a_e) * d_e)))

        return new_lines

    # Повернуть все относительно точки (rotate all from point)
    def rafp(self, angle, pos: Pos):
        angles = []
        for i in self.lines:
            angles.append([i.get_angle_of_sp(pos), Line(pos, i.start).get_distance()])
        for i in angles:
            i[0] += angle
        new_lines = []
        for i in range(len(angles)):
            d_e = self.lines[i].get_distance()
            a_e = self.lines[i].get_angle_of_ep(self.lines[i].start) + angle
            a_s = angles[i][0]
            d_s = angles[i][1]
            print(d_s)
            p_s = Pos(math.cos(a_s) * d_s, math.sin(a_s) * d_s) + pos
            new_lines.append(Line(p_s, p_s + Pos(math.cos(a_e) * d_e, math.sin(a_e) * d_e)))

        return new_lines

    def draw_map(self, display: pg.Surface):
        for i in self.lines:
            i.draw_on_map(display)

    def collide_with_two(self, l1i, l2i, r=False):
        l1 = self.lines[l1i]
        l2 = self.lines[l2i]
        if l1.start > l2.start > l1.end or l1.start > l2.end > l1.end or \
                l1.start < l2.start < l1.end or l1.start < l2.end < l1.end:
            angle = -l1.get_angle_of_ep(l1.start)
            mp = self.rafp(angle, l1.start)
            l1 = mp[l1i]
            l2 = mp[l2i]
            if l2.start.x < l1.start.x < l2.end.x:
                return Pos(l1.start.x, (l2.get_normalized().y / l2.get_normalized().x) * l1.start.x)
            if l2.start.y < l1.start.y < l2.end.y:
                return Pos((l2.get_normalized().x / l2.get_normalized().y) * l1.start.y, l1.start.y)
        if not r:
            return self.collide_with_two(l2i, l1i, r=True)
        return False
