from config import *
from classes.object import Pos, Line
from classes.map import Map
from classes.player import Player
import math
import pygame as pg

pg.init()


class Game:
    def __init__(self, player: Player, map: Map, max_speed, sensitivity):
        pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.pl = player
        self.map = map
        self.run = True
        self.display = pg.display.set_mode([WIDTH, HEIGHT], pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.max_speed = max_speed
        self.speed = max_speed / FPS
        self.sensitivity = sensitivity
        self.motion = {'left': False, 'right': False, 'forward': False, 'backward': False}

    def events(self):
        for i in pg.event.get():
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_w:
                    self.motion['forward'] = True
                if i.key == pg.K_s:
                    self.motion['backward'] = True
                if i.key == pg.K_a:
                    self.motion['left'] = True
                if i.key == pg.K_d:
                    self.motion['right'] = True

                if i.key == pg.K_ESCAPE:
                    self.run = False
            elif i.type == pg.KEYUP:
                if i.key == pg.K_w:
                    self.motion['forward'] = False
                if i.key == pg.K_s:
                    self.motion['backward'] = False
                if i.key == pg.K_a:
                    self.motion['left'] = False
                if i.key == pg.K_d:
                    self.motion['right'] = False
            if i.type == pg.MOUSEMOTION:
                new_pos = pg.mouse.get_pos()[0]
                if new_pos != WIDTH // 2:
                    self.pl.angle += math.pi / 2 * ((new_pos - WIDTH / 2) / WIDTH)
                    pg.mouse.set_pos([WIDTH // 2, HEIGHT // 2])

    def update(self, frames):
        self.pl.draw(self.display, self.map)
        if frames != 0:
            self.speed = self.max_speed / frames

        if self.motion['forward']:
            self.pl.move(self.map, Pos(math.cos(self.pl.angle) * self.speed, math.sin(self.pl.angle) * self.speed))
        elif self.motion['backward']:
            self.pl.move(self.map, Pos(-math.cos(self.pl.angle) * self.speed, -math.sin(self.pl.angle) * self.speed))

        if self.motion['left']:
            self.pl.move(self.map, Pos(math.cos(self.pl.angle - math.pi / 2) * self.speed,
                                       math.sin(self.pl.angle - math.pi / 2) * self.speed))
        elif self.motion['right']:
            self.pl.move(self.map, Pos(math.cos(self.pl.angle + math.pi / 2) * self.speed,
                                       math.sin(self.pl.angle + math.pi / 2) * self.speed))

    def draw(self, frames):
        self.display.fill([255, 255, 255])
        if frames != 0:
            text = FONT.render(f'FPS: {frames}', True, (255, 0, 0))
            self.display.blit(text, (0, 0))
        self.pl.draw(self.display, self.map)

    def start_cycle(self):
        while self.run:
            frames = self.clock.get_fps()
            self.events()
            self.update(frames)
            self.draw(frames)
            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()


if __name__ == '__main__':
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
    map = Map(lines)
    pl = Player(Pos(25, 50))
    pl.angle += math.pi
    game = Game(pl, map, 60, 100)
    game.start_cycle()
