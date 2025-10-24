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
light_angle = 0
width = 60

image = pg.image.load("image.jpeg")
image = pg.transform.scale(image, SCREEN_SIZE)
mask_surface = pg.Surface(SCREEN_SIZE, pg.SRCALPHA)


light = pg.image.load("light.png").convert_alpha()
light = pg.transform.scale(light, (100, 100))
light = pg.transform.flip(light, True, False)

print("НАЖМИТЕ E ДЛЯ РАСШИРЕНИЯ УГЛА")
print("НАЖМИТЕ R ДЛЯ ПОВОРОТА УГЛА")
print("ДВИГАЙТЕ ЛУЧ ПО СТРЕЛОЧКАМ")
print("*убедитесь что у вас английская раскладка")



running = True
flag = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    SCREEN.fill('black')
    ans = get_crosses(ray_x, ray_y, light_angle, width)
    verticies = [(ray_x, ray_y)] + [(cross.x, cross.y) for cross in ans]
    # pg.draw.polygon(SCREEN, 'yellow', verticies)
    mask_surface.fill((0, 0, 0, 0))
    pg.draw.polygon(mask_surface, (255, 255, 255, 255), verticies)
    
    mask = pg.mask.from_surface(mask_surface)
    masked_image_surface = pg.Surface(image.get_size(), pg.SRCALPHA)
    masked_image_surface.blit(image, (0, 0)) 
    masked_image_surface.blit(mask_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    SCREEN.blit(masked_image_surface, (0, 0))
    # for v in ans:
    #     if v:
    #         pg.draw.line(SCREEN, 'red', (ray_x, ray_y), (v.x, v.y), 1)
    keys = pg.key.get_pressed() 
    if keys[pg.K_LEFT]:
        ray_x = max(ray_x - 5, 5)
    if keys[pg.K_RIGHT]:
        ray_x = min(ray_x + 5, SCREEN_SIZE[0] - 5)
    if keys[pg.K_UP]:
        ray_y = max(ray_y - 5, 5)
    if keys[pg.K_DOWN]:
        ray_y = min(ray_y + 5, SCREEN_SIZE[1] - 5)
    if keys[pg.K_r]:
        light_angle = (light_angle + 5) % 360
    if keys[pg.K_e]:
        width = 1 + (min(width + 1, 180)) % 180
    for segment in segments:
        pg.draw.line(SCREEN, 'blue', (segment.point1.x, segment.point1.y), (segment.point2.x, segment.point2.y), 3)
    # pg.draw.circle(SCREEN, 'red', (ray_x, ray_y), 5)
    copy = pg.transform.rotate(light, -light_angle + 20)
    SCREEN.blit(copy, (ray_x-65, ray_y-75))
    pg.display.update()
    clock.tick(FPS)
pg.quit()


