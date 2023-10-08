from classes.line import *
from classes.object import *
from config import *


class Camera:
    def __init__(self, pos: Pos, fov: int=90, lov: int = 50):
        self.pos = pos
        # Угол обзора (field of view)
        self.fov = fov
        # Кол-во линий (amount of lines)
        self.aol = WIDTH
        self.lines = []
        for i in range(self.aol):
            self.lines.append(Line(self.pos))


