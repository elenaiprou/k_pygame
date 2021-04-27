import pygame as pg
import sys
from random import randint

def rebotaX(x):
    if x<=0 or x >= ANCHO:
        return -1

    return 1

def rebotaY(y):
    if y<=0 or y >= ALTO:
        return -1

    return 1

#declaración colores para que sea más fácil usar durante el juego
Rojo = (255, 0, 0)
Azul = (0, 0, 255)
Verde = (0, 255, 0)
Negro = (0, 0, 0)

ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))
reloj = pg.time.Clock() #ayuda a relentizar cada vuelta de bucle

bolas = []
for _ in range(10):
    bola = {'x': randint(0, ANCHO),
            'y': randint(0, ALTO),
            'vx': randint(5, 15),
            'vy': randint(5, 15),
            'color': (randint(0, 255), randint(0,255), randint(0,255))
    }
    bolas.append(bola)

game_over = False
while not game_over:
    reloj.tick(60) #con este comando dices cada cuanto quieres que se actualicen los eventos    
    #gestion eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True

    #modificacion de estado 
    for bola in bolas:
        bola['x'] += bola['vx']
        bola['y'] += bola['vy']

        bola['vy'] *= rebotaY(bola['y'])
        bola['vx'] *= rebotaX(bola['x'])

    #gestion pantalla
    pantalla.fill(Negro)
    for bola in bolas:
        pg.draw.circle(pantalla, bola['color'], (bola['x'], bola['y']), 10)


    pg.display.flip()


pg.quit()
sys.exit()
