import pygame as pg
import sys
import random

ANCHO = 800
ALTO = 400
FPS = 60

bola = Bola()

class Bola(pg.sprite.Sprite): #el primer sprite es el modulo, el Sprite (mayuscula) es la clase
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # super().__init__() es lo mismo que arriba.
        self.image = pg.image.load('./iamges/ball1.png').convert_alpha() #calcomania, la imagen de la pelota
        self.rect = self.image.get_rect(center=(x,y)) #rectangulo nos dará la imagen que hemos guardado, y en este tamaño que tenga la imagen guardada.

        self.vx = random.randint(5, 10)*random.choice((-1, 1))
        self.vy = random.randint(5, 10)*random.choice((-1, 1))

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vy *= -1

class Game():
    def __init__(self): #los atributos se crean dentro del la funcion constructor (def __init__)
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.botes = 0

        self.bola = Bola(ANCHO//2, ALTO//2)

    def bucle_principal(self):
        game_over = False #sin self delante pq es una variable y no un atributo, que además no tiene sentido en otro lugar.
        reloj = pg.time.Clock()
        while not game_over:
            reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
                
            self.bola.update()

            self.pantalla.fill((0, 0, 0))
            self.pantalla.blit(self.bola.image, self.bola.rect.topleft)
            