import math
import pygame as pg
from config import *
from classes.object import *
from classes.line import *
from classes.map import *

pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

run = True

map = Map([Line(Pos(500, 500), Pos(500, 700)), Line(Pos(700, 200), Pos(200, 700))], None)
while run:
    display.fill([255, 255, 255])
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
    map.draw_map(display)
    c = map.collide_with_two(0, 1)
    if c:
        c.draw_on_map(display, [255, 0, 0])

    pg.display.update()
    clock.tick(FPS)
