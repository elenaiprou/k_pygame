import pygame as pg
import sys
#declaración colores para que sea más fácil usar durante el juego
Rojo = (255, 0, 0)
Azul = (0, 0, 255)
Verde = (0, 255, 0)
Negro = (0, 0, 0)

ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))

game_over = False
x = ANCHO // 2 # Dos divisiones no dan numeros decimales
y = ALTO // 2

vx = -2 #variable velocidad en X
vy = -2 #variable velocidad en Y
while not game_over:
    #gestion eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True

    #modificacion de estado 
    x += vx
    y += vy

    if y == 0:
        vy = 2

    if y == ALTO:
        vy = -2

    if x == 0:
        vx = 2

    if x == ANCHO:
        vx = -2   
    
    #gestion pantalla
    pantalla.fill(Negro)
    pg.draw.circle(pantalla, Rojo, (x,y), 10)

    pg.display.flip()


pg.quit()
sys.exit()
