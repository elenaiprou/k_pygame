import pygame as pg
import sys
from random import randint, choice



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


class Bola():
    def __init__(self, x, y, vx=5, vy=5, color=(255,255,255), radio=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio

    def actualizar(self): #las bolas rebotan y son ellas mismas que comprueban que no salen de los bordes, y se actualiza para moverse
        self.x += self.vx
        self.y += self.vy

        if self.x<=0 or self.x >= ANCHO:
            self.vx = -self.vx

        if self.y<=0 or self.y >= ALTO:
            self.vy = -self.vy
    
    def dibujar(self, lienzo):
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.radio)


bolas = []
for _ in range(10):
    bola = Bola(randint(0, ANCHO),
                randint(0, ALTO),
                randint(5, 10)*choice([-1,1]),
                randint(5, 10)*choice([-1,1]),
                (randint(0, 255), randint(0,255), randint(0,255)),
                randint(5, 20))

    bolas.append(bola)

game_over = False
while not game_over:
    v = reloj.tick(60)
    #Gestion de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # Modificación de estado
    for bola in bolas:
        bola.actualizar()


    # Gestión de la pantalla
    pantalla.fill(Negro)
    for bola in bolas:
        bola.dibujar(pantalla)
        

    pg.display.flip()


pg.quit()
sys.exit()
