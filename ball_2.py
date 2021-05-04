import pygame as pg
import sys
import random

ANCHO = 800
ALTO = 600
FPS = 60

class Marcado():
    def __init__(self, x, y, fontsize = 25, color=(255, 255, 255)):
        self.fuente = pg.font.SysFont("Arial", fontsize)
        self.x = x
        self.y = y
        self.color = color
    
    def dibuja (self, text, lienzo):
        image = self.fuente.render(str(text), True, self.color)
        lienzo.blit(image, (self.x, self.y))

class Bola(pg.sprite.Sprite): #el primer sprite es el modulo, el Sprite (mayuscula) es la clase
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # super().__init__() es lo mismo que arriba.
        self.image = pg.image.load('./images/ball1.png').convert_alpha() #calcomania, la imagen de la pelota
        self.rect = self.image.get_rect(center=(x,y)) #rectangulo nos dará la imagen que hemos guardado, y en este tamaño que tenga la imagen guardada.

        self.vx = random.randint(5, 10)*random.choice((-1, 1))
        self.vy = random.randint(5, 10)*random.choice((-1, 1))

    def update(self): #controla la posicion de la bola, si choca con los limites cambia la posición y velocidad
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
        self.cuentaGolpes = Marcado(10, 10)

        self.ballGroup =pg.sprite.Group() #creamos de 1 a 20 bolas
        for i in range(random.randint(1, 20)):
            bola = Bola(random.randint(0, ANCHO), random.randint(0, ALTO))
            self.ballGroup.add(bola)

        '''
        self.bola = Bola(ANCHO//2, ALTO//2) #estas colocando una bola en el centro de la pantalla. 
        '''

    def bucle_principal(self):
        game_over = False #sin self delante pq es una variable y no un atributo, que además no tiene sentido en otro lugar.
        reloj = pg.time.Clock()
        while not game_over:
            reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
                
            # self.bola.update() actualiza una bola
            self.ballGroup.update()

            self.pantalla.fill((0, 0, 0))
            self.cuentaGolpes.dibuja('Hola', self.pantalla)
            # self.pantalla.blit(self.bola.image, self.bola.rect.topleft) para una bola
            self.ballGroup.draw(self.pantalla)

            pg.display.flip()

#ahora se han de instancializar las clases
if __name__ == '__main__':
    pg.init()
    game = Game() #instanciar game
    game.bucle_principal() #llamar al juego, la clase Game ya llama a Bola, por eso no se ha de llamar aquí.
