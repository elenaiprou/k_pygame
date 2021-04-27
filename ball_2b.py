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

#Bola1
x = ANCHO // 2 # Dos divisiones no dan numeros decimales
y = ALTO // 2
vx = -7 #variable velocidad en X
vy = -7 #variable velocidad en Y

#Bola 2
x2 = randint(0, ANCHO)
y2 = randint(0, ALTO)
vx2 = randint(5, 15)
vy2 = randint(5, 15)

game_over = False
while not game_over:
    reloj.tick(60) #con este comando dices cada cuanto quieres que se actualicen los eventos    
    #gestion eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True

    #modificacion de estado 
    x += vx
    y += vy
    x2 += vx2
    y2 += vy2

    vy *= rebotaY(y)
    vx *= rebotaX(x)

    vy2 *= rebotaY(y2)
    vx2 *= rebotaX(x2)


    
    #gestion pantalla
    pantalla.fill(Negro)
    pg.draw.circle(pantalla, Rojo, (x,y), 10)
    pg.draw.circle(pantalla, Verde, (x2,y2), 10)

    pg.display.flip()


pg.quit()
sys.exit()
