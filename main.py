import pygame as pg
from geometry import *
from math import hypot, radians, atan, degrees
from random import randint

pg.init()
SCREEN_SIZE = (800, 600)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
FPS = 60
clock = pg.time.Clock()

ray_x, ray_y = 50, 50

running = True
flag = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            flag = True
        elif event.type == pg.KEYUP:
            flag = False
        
    SCREEN.fill('black')
    ans = get_crosses(ray_x, ray_y)
    verticies = [(cross.x, cross.y) for cross in ans]
    pg.draw.polygon(SCREEN, 'yellow', verticies)
    for v in ans:
        if v:
            pg.draw.line(SCREEN, 'red', (ray_x, ray_y), (v.x, v.y), 1)
    if flag:
        if event.key == pg.K_LEFT:
            ray_x = max(ray_x - 5, 5)
        if event.key == pg.K_RIGHT:
            ray_x = min(ray_x + 5, SCREEN_SIZE[0] - 5)
        if event.key == pg.K_UP:
            ray_y = max(ray_y - 5, 5)
        if event.key == pg.K_DOWN:
            ray_y = min(ray_y + 5, SCREEN_SIZE[1] - 5)
    for segment in segments:
        pg.draw.line(SCREEN, 'blue', (segment.point1.x, segment.point1.y), (segment.point2.x, segment.point2.y), 3)
    pg.draw.circle(SCREEN, 'red', (ray_x, ray_y), 5)
    

    pg.display.update()
    clock.tick(FPS)
pg.quit()


