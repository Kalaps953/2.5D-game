import pygame as pg
from config import *
from classes.object import *
from classes.line import *


pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

run = True

line1 = Line(Pos(20, 20), Pos(100, 100), 1, [0, 0, 0])
line2 = Line(Pos(10, 50), Pos(200, 10), 2, [255, 0, 0])

while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False

    display.fill([255, 255, 255])

    line1.draw_on_map(display)
    line2.draw_on_map(display)
    p = line1.collide(line2)
    if p:
        p[1].draw_on_map(display, [0, 128, 0])
        print(p[1])
        p[2].draw_on_map(display, [0, 255, 0])
        print(p[2])
        p[3].draw_on_map(display, [0, 0, 255])
        print(p[3])

    pg.display.update()
    clock.tick(FPS)

