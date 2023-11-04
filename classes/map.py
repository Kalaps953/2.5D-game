from classes.camera import *
from classes.object import *
import pygame as pg


class Map:
    def __init__(self, lines: list, camera):
        self.lines = lines
        self.camera = camera

    def draw_map(self, display: pg.Surface):
        for i in self.lines:
            i.draw_on_map(display)

    def get_rotated(self, angle: float, pos: Pos):
        lines = []
        for i in self.lines:
            lines.append(i.get_rotated(angle, pos))
        return Map(lines, self.camera)
