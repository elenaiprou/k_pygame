import pygame as pg
import sys
import random
from enum import Enum

ANCHO = 800
ALTO = 600
FPS = 60

class Marcador_tipoH(pg.sprite.Sprite):
    plantilla = "{}"

    def __init__(self, x, y, justificado = "topleft", fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = ""
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        #self.image = self.fuente.render(str(self.text), True, self.color)
        self.image = None
        self.rect = None

    def update(self, dt):
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class CuentaVidas(Marcador_tipoH): #no me sale la palabra vidas, revisarlo!!!!
    plantilla = "Vidas: {}"

class Marcador(pg.sprite.Sprite): #usamos el otro marcador porque es mas bonito el codigo

    class Justificado():
        izquierda = "I"
        derecha = "D"
        centrado = "C"

    def __init__(self, x, y, justificado = None, fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.SysFont("Arial", fontsize)
        self.text = "0"
        self.color = color
        self.x = x
        self.y = y
        if not justificado:
            self.justificado = Marcador.Justificado.izquierda
        else:
            self.Justificado = justificado

        # self.image = self.fuente.render(str(self.text), True, self.color) Esto lo ha eliminado

        self.image = None
        self.rect = None

    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color)
        if self.justificado == Marcador.Justificado.izquierda:
            self.rect = self.image.get_rect(topleft =(self.x, self.y))
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright =(self.x, self.y))
        else:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Ladrillo(pg.sprite.Sprite): #revisar pq no desaparecen los ladrillos cuando le pega la pelota
    disfraces = ['greenTile.png', 'redTile.png', 'redTileBreak.png']

    def __init__(self, x, y, esDuro=False):
        super().__init__()
        self.imaganes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if self.esDuro else 0 #operador ternario
        self.image = self.imaganes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.numGolpes = 0
    
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes
    
    def update(self, dt):
        if self.esDuro and self.numGolpes ==1:
            self.imagen_actual = 2
            self.image = self.imaganes[self.imagen_actual]
    
    def desaparece(self):
        self.numGolpes +=1
        # return (self.numGolpes >1 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro)
        #este return de arriba es lo mismo que el if de a bajo comentado        
        
        if (self.numGolpes == 1 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro):
            return True
        else:
            return False


class Raqueta(pg.sprite.Sprite):
    disfraces = ['electric00.png', 'electric01.png', 'electric02.png']
    def __init__(self, x, y, w=ANCHO, h = 30):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 5
        self.milisegundos_acumulados = 0
        
        # self.image = pg.Surface((w, h), pg.SRCALPHA, 32) #pg.SRCALPHA creamos superficie transparente
        # pg.draw.rect(self.image, (255, 0, 0), pg.Rect(0, 0, w, h)) #hemos hecho el dibujito
        # self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes

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

        self.milisegundos_acumulados += dt
        if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
            self.imagen_actual += 1
            if self.imagen_actual >= len(self.disfraces):
                self.imagen_actual = 0
            self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]

class Bola(pg.sprite.Sprite):
    disfraces = ['ball1.png', 'ball2.png', 'ball3.png', 'ball4.png', 'ball5.png']

    class Estado_bola(Enum): #solo se usa la clase Estado_bola en la clase Bola, la Raqueta no la puede usar.
        viva = 0
        agonizando = 1
        muerta = 2

    def __init__(self, x, y,):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]
        self.milisegundos_acumulados = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 10
        self.rect = self.image.get_rect(center=(x,y))
        self.xOriginal = x
        self.yOriginal = y
        self.estado = Bola.Estado_bola.viva
        
        self.vx = random.randint(2, 5) * random.choice([-1, 1])
        self.vy = random.randint(2, 5) * random.choice([-1, 1])

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./images/{}".format(fichero)))
        return imagenes

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos

    def update(self, dt):
        if self.estado == Bola.Estado_bola.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1 
            if self.rect.top <= 0:
                self.vy *= -1

            if self.rect.bottom >= ALTO: 
                self.estado = Bola.Estado_bola.agonizando
                self.rect.bottom = ALTO
        elif self.estado == Bola.Estado_bola.agonizando:
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0
                if self.imagen_actual >= len(self.disfraces):
                    self.estado = Bola.Estado_bola.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]
        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(2, 5) * random.choice([-1, 1])
            self.vy = random.randint(2, 5) * random.choice([-1, 1])
            self.estado = Bola.Estado_bola.viva

class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.puntuacion = 0
        self.todoGrupo = pg.sprite.Group()
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()

        level1 = ['XXXXXXXX', 
        'X--DD--X',           
        'X--DD--X',           
        'XXXXXXXX']

        esDuro = False
        for fila in range(len(level1)):
            for columna in range(8):
                    fila2 = level1[fila]
                    columna2 = fila2[columna]
                    x = columna * 100 + 5
                    y = fila * 40 + 5
                    if columna2 == "-":
                        False
                    elif columna2 == "D":
                        esDuro = True
                        ladrillo = Ladrillo(x, y, esDuro)
                        self.grupoLadrillos.add(ladrillo)
                    else:
                        esDuro = False
                        ladrillo = Ladrillo(x, y, esDuro)
                        self.grupoLadrillos.add(ladrillo)
        
        # for fila in range(4):
        #     for columna in range(8):
        #         x = columna * 100 + 5
        #         y = fila * 40 + 5 
        #         esDuro = random.randint(1, 10) == 1
        #         ladrillo = Ladrillo(x, y, esDuro)
        #         self.grupoLadrillos.add(ladrillo)

        self.cuentaPuntos = Marcador_tipoH(10,10, fontsize=50)
        self.cuentaVidas = CuentaVidas(790, 10, 'topright', 50, (255, 255, 0)) 
        self.fondo = pg.image.load("./images/background.png")

        self.bola = Bola(ANCHO // 2, ALTO // 2)
        self.todoGrupo.add(self.bola)    

        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)

        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)

    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        

        while not game_over and self.vidas > 0: 
            dt = reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True

            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas
            self.bola.prueba_colision(self.grupoJugador)
            tocados = self.bola.prueba_colision(self.grupoLadrillos)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece():
                    self.grupoLadrillos.remove(ladrillo)
                    self.todoGrupo.remove(ladrillo)

            self.todoGrupo.update(dt)
            if self.bola.estado == Bola.Estado_bola.muerta:
                self.vidas -= 1

            self.pantalla.blit(self.fondo, (0,0))
            self.todoGrupo.draw(self.pantalla)

            pg.display.flip()

if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bucle_principal()