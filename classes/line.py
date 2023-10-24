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
        return f's= ({self.start});; e= ({self.end});'

    def get_distance(self):
        d = (self.start - self.end) ** 2
        return math.sqrt(d.x + d.y)

    def get_normalized(self):
        return (self.end - self.start) / self.get_distance()

    def draw_on_map(self, display: pg.Surface):
        print(self)
        pg.draw.line(display, self.color, self.start.get_arr(), self.end.get_arr())

    def __add__(self, other):
        if isinstance(other, Pos):
            return Line(self.start + other, self.end + other)

    def get_angle_of_sp(self, pos):
        if Line(pos, self.start).get_distance() != 0:
            norm = Line(pos, self.start).get_normalized()
            angle = math.asin(norm.y)
            if norm.x < 0:
                return math.pi / 2 - angle + math.pi / 2
            return angle
        return 0

    def get_angle_of_ep(self, pos):
        norm = Line(pos, self.end).get_normalized()
        angle = math.asin(norm.y)
        if norm.x < 0:
            return math.pi / 2 - angle + math.pi / 2
        return angle
