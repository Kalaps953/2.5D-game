from config import *
from classes.object import Pos, Line
from classes.map import Map
from classes.player import Player
import math
import pygame as pg

pg.init()

display = pg.display.set_mode([WIDTH, HEIGHT], pg.FULLSCREEN)
pg.mouse.set_visible(False)
clock = pg.time.Clock()

run = True

lines = [Line(Pos(0, 0), Pos(250, 0)),
         Line(Pos(0, 0), Pos(0, 250)),
         Line(Pos(250, 250), Pos(250, 0)),
         Line(Pos(250, 250), Pos(50, 250)),

         Line(Pos(50, 0), Pos(50, 100)),
         Line(Pos(50, 100), Pos(100, 100)),
         Line(Pos(100, 0), Pos(100, 50)),
         Line(Pos(150, 0), Pos(150, 100)),
         Line(Pos(150, 100), Pos(200, 100)),
         Line(Pos(200, 100), Pos(200, 50)),
         Line(Pos(0, 150), Pos(200, 150)),
         Line(Pos(100, 150), Pos(100, 200)),
         Line(Pos(200, 150), Pos(200, 200)),
         Line(Pos(100, 150), Pos(100, 200)),
         Line(Pos(100, 200), Pos(200, 200))]
print(len(lines))
map = Map(lines)
pl = Player(Pos(25, 25))
speed = 2
motion = {'forward': False, 'backward': False, 'left': False, 'right': False}
pg.mouse.set_pos([WIDTH // 2, 0])
while run:
    f = clock.get_fps()
    display.fill([255, 255, 255])
    if f != 0:
        speed = 60 / f
        text = FONT.render(f'FPS: {f}', True, (255, 0, 0))
        display.blit(text, (0, 0))
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_w:
                motion['forward'] = True
            if i.key == pg.K_s:
                motion['backward'] = True
            if i.key == pg.K_a:
                motion['left'] = True
            if i.key == pg.K_d:
                motion['right'] = True

            if i.key == pg.K_ESCAPE:
                run = False
        elif i.type == pg.KEYUP:
            if i.key == pg.K_w:
                motion['forward'] = False
            if i.key == pg.K_s:
                motion['backward'] = False
            if i.key == pg.K_a:
                motion['left'] = False
            if i.key == pg.K_d:
                motion['right'] = False
        if i.type == pg.MOUSEMOTION:
            new_pos = pg.mouse.get_pos()[0]
            if new_pos != WIDTH // 2:
                pl.angle += math.pi / 2 * ((new_pos - WIDTH / 2) / WIDTH)
                pg.mouse.set_pos([WIDTH // 2, HEIGHT // 2])

    if motion['forward'] and not motion['backward']:
        pl.move(map, Pos(math.cos(pl.angle) * speed, math.sin(pl.angle) * speed))
    elif motion['backward'] and not motion['forward']:
        pl.move(map, Pos(math.cos(pl.angle) * -speed, math.sin(pl.angle) * -speed))
    if motion['left']:
        pl.move(map, Pos(math.cos(pl.angle - math.pi / 2) * speed,
                                   math.sin(pl.angle - math.pi / 2) * speed))
    elif motion['right']:
        pl.move(map, Pos(math.cos(pl.angle + math.pi / 2) * speed,
                                   math.sin(pl.angle + math.pi / 2) * speed))

    pl.draw(display, map)
    pg.draw.circle(display, [255, 0, 0], [WIDTH // 2, HEIGHT // 2], 5)
    pg.display.update()
    clock.tick(FPS)
