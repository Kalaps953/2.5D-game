import math
import pygame as pg
from config import *
from classes.object import Pos, Line
from classes.map import Map

pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

run = True

map = Map([Line(Pos(250, 500), Pos(750, 500)), Line(Pos(500, 250), Pos(900, 750))], None)
while run:
    display.fill([255, 255, 255])
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
    map.draw_map(display)
    p = map.lines[0].collide(map.lines[1])
    if p:
        p.draw(display, [255, 0, 0])
        print(p)

    pg.display.update()
    clock.tick(FPS)
