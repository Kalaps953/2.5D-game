import math
import pygame as pg
from config import *
from classes.object import Pos, Line
from classes.map import Map
from classes.player import Player

pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

run = True

lines = [Line(Pos(0, 0), Pos(100, 100)),
         Line(Pos(100, 100), Pos(0, 200)),
         Line(Pos(0, 200), Pos(-100, 100)),
         Line(Pos(-100, 100), Pos(0, 0))]
map = Map(lines)
pl = Player(Pos(0, 100))
pl.angle += math.pi / 4

motion = {'left': False, 'right': False, 'forward': False, 'backward': False}
without = False

speed = 120 / FPS
while run:
    display.fill([255, 255, 255])
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_a:
                motion['left'] = True
            if i.key == pg.K_d:
                motion['right'] = True
            if i.key == pg.K_w:
                motion['forward'] = True
            if i.key == pg.K_s:
                motion['backward'] = True

            if i.key == pg.K_SPACE:
                without = True

            if i.key == pg.K_ESCAPE:
                run = False
        elif i.type == pg.KEYUP:
            if i.key == pg.K_a:
                motion['left'] = False
            if i.key == pg.K_d:
                motion['right'] = False
            if i.key == pg.K_w:
                motion['forward'] = False
            if i.key == pg.K_s:
                motion['backward'] = False
            if i.key == pg.K_SPACE:
                without = False
    if motion['left'] and not motion['right']:
        pl.angle -= math.pi / FPS
    elif motion['right'] and not motion['left']:
        pl.angle += math.pi / FPS

    if motion['forward'] and not motion['backward']:
        pl.pos += Pos(math.cos(pl.angle) * speed, math.sin(pl.angle) * speed)
    elif motion['backward'] and not motion['forward']:
        pl.pos -= Pos(math.cos(pl.angle) * speed, math.sin(pl.angle) * speed)

    pl.draw(display, map, without)
    pl.draw_lines(display)
    map.draw_map(display)
    pg.display.update()
    clock.tick(FPS)
