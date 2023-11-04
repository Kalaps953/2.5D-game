import math
import pygame as pg
from config import *
from classes.object import Pos, Line
from classes.map import Map
from classes.camera import Camera

pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

run = True

map = Map([Line(Pos(250, 500), Pos(750, 500)), Line(Pos(500, 250), Pos(900, 750))])
cam = Camera(Pos(500, 700))

while run:
    display.fill([255, 255, 255])
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
    cam.draw(display, map)
    map.draw_map(display)

    pg.display.update()
    clock.tick(FPS)
