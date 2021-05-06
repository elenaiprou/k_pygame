import pygame as pg
import sys
import random

ANCHO = 800
ALTO = 600
FPS = 60

class Marcado(pg.sprite.Sprite):
    def __init__(self, x, y, fontsize = 25, color=(255, 255, 255)):
        pg.sprite.Sprite.__init__(self)
        self.fuente = pg.font.SysFont("Arial", fontsize)
        self.text = "0"
        self.color = color
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self, dt):#importante poner "updated" para actualizar, poner en cada grupo 
        self.image = self.fuente.render(str(self.text), True, self.color)


class Raqueta(pg.sprite.Sprite):
    fotos = ['electric00.png', 'electric01.png', 'electric02.png']

    def __init__(self, x, y, w=100, h=30):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h), pg.SRCALPHA, 32) #pg.SRCALPHA creamos superficie transparente
        pg.draw.rect(self.image, (255, 0, 0), pg.Rect(0, 0, w, h)) #hemos hecho el dibujito
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7
    
    def update(self, dt):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_LEFT]:
            self.rect.x -= self.vx

        if teclas_pulsadas[pg.K_RIGHT]:
            self.rect.x += self.vx

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO


class Bola(pg.sprite.Sprite): #el primer sprite es el modulo, el Sprite (mayuscula) es la clase
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # super().__init__() es lo mismo que arriba.
        self.image = pg.image.load('./images/ball1.png').convert_alpha() #calcomania, la imagen de la pelota
        self.rect = self.image.get_rect(center=(x,y)) #rectangulo nos dará la imagen que hemos guardado, y en este tamaño que tenga la imagen guardada.

        self.vx = random.randint(5, 10)*random.choice((-1, 1))
        self.vy = random.randint(5, 10)*random.choice((-1, 1))

    def update(self, dt): #controla la posicion de la bola, si choca con los limites cambia la posición y velocidad
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
        self.todoGroup =pg.sprite.Group() #creamos de 1 a 20 bolas
        
        self.cuentaSegundos = Marcado(10, 10)
        self.todoGroup.add((self.cuentaSegundos))
        
        self.bola = Bola(random.randint(0, ANCHO), random.randint(0, ALTO))
        self.todoGroup.add(self.bola)
        
        self.raqueta = Raqueta(x = ANCHO//2, y= ALTO-14)
        self.todoGroup.add(self.raqueta)

    def bucle_principal(self):
        game_over = False #sin self delante pq es una variable y no un atributo, que además no tiene sentido en otro lugar.
        reloj = pg.time.Clock()
        contador_milisegundos = 0
        segundero = 0
        while not game_over:
            dt = reloj.tick(FPS)
            contador_milisegundos += dt

        if contador_milisegundos >= 1000:
            segundero += 1
            contador_milisegundos = 0

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True
                
            # self.bola.update() actualiza una bola
            self.cuentaSegundos.text = segundero
            self.todoGroup.update()

            self.pantalla.fill((0, 0, 0))
            #self.cuentaGolpes.dibuja('Hola', self.pantalla)
            # self.pantalla.blit(self.bola.image, self.bola.rect.topleft) para una bola
            self.todoGroup.draw(self.pantalla)

            pg.display.flip()

#ahora se han de instancializar las clases
if __name__ == '__main__':
    pg.init()
    game = Game() #instanciar game
    game.bucle_principal() #llamar al juego, la clase Game ya llama a Bola, por eso no se ha de llamar aquí.
