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

myfont = pg.font.SysFont("Arial", 32)
textX = 10
textY = 10
vidasT = 3

def muestra_vidas(x,y):
    contador = myfont.render("Vidas: " +str(vidasT), True, Rojo)
    screen.blit(contador, (x, y))

class Bola():
    def __init__(self, x, y, vx, vy, color=(255,255,255), radio=10):
        self.x = x #posición
        self.y = y #posición
        self.vx = vx #movimiento, velocidad
        self.vy = vy #movimiento, velocidad
        self.color = color
        self.anchura = radio*2
        self.altura = radio*2

    def actualizar(self): #las bolas rebotan y son ellas mismas que comprueban que no salen de los bordes, y se actualiza para moverse
        self.x += self.vx
        self.y += self.vy

        if self.x<=0 or self.x >= ANCHO:
            self.vx = -self.vx

        if self.y<=0:
            self.vy = -self.vy

        if self.y >= ALTO:
            self.x = ANCHO //2
            self.y = ALTO // 2
            return True
        return False
    
    def dibujar(self, lienzo):
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.anchura//2)
    
    def comprueba_colision (self, objeto):
        '''
        if self.x >= objeto.x and self.x <= objeto.x+objeto.anchura or \
            self.x+self.anchura >= objeto.x and self.x+self.anchura <= objeto.x + objeto.anchura:
            choqueX = True
        else:
            choqueX = False
        '''
        choqueX = self.x >= objeto.x and self.x <= objeto.x+objeto.anchura or \
            self.x+self.anchura >= objeto.x and self.x+self.anchura <= objeto.x + objeto.anchura
        choqueY = self.y >= objeto.y and self.y <= objeto.y+objeto.altura or \
            self.y+self.altura >= objeto.y and self.y+self.altura <= objeto.y + objeto.altura
        if choqueX and choqueY:
            self.vy *= -1


class Raqueta():
    def __init__(self, x=0, y=0):
        self.altura = 10
        self.anchura = 100
        self.color = (255, 255, 255)
        self.x = (ANCHO - self.anchura) // 2
        self.y = ALTO - self.altura - 15 #restamos 15 para separarlo del final
        self.vy = 0
        self.vx = 13
    
    def dibujar(self, lienzo):
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(lienzo, self.color, rect)
    
    def actualizar(self):
        teclas_pulsadas = pg.key.get_pressed()

        if teclas_pulsadas[pg.K_LEFT] and self.x > 0:
            self.x -= self.vx
        if teclas_pulsadas[pg.K_RIGHT] and self.x < ANCHO - self.anchura: 
            self.x += self.vx


bola = Bola(randint(0, ANCHO), #llamar una bola
            randint(0, ALTO),
            randint(4, 7)*choice([-1,1]),
            randint(4, 7)*choice([-1,1]),
            (randint(0, 255), randint(0,255), randint(0,255)))

raqueta = Raqueta() #llamar a la raqueta

game_over = False
while not game_over:
    v = reloj.tick(60)
    #Gestion de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # Modificación de estado
    raqueta.actualizar()
    bola.comprueba_colision(raqueta)
    pierdebola = bola.actualizar()
    if pierdebola:
        vidasT -= 1
        print (vidasT)
    elif vidasT ==0:
        print ("game over")
        pg.quit()
        sys.exit()

    # Gestión de la pantalla
    pantalla.fill(Negro)
    bola.dibujar(pantalla)
    raqueta.dibujar(pantalla)
    muestra_vidas((textX, textY))

    pg.display.flip()
    if pierdebola:
        pg.time.delay(500)


pg.quit()
sys.exit()
