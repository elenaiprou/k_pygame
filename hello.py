import pygame as pg
import sys

pg.init() # Inicializar todos los controles de pygame
pantalla = pg.display.set_mode((600,400))
pg.display.set_caption("Hola")

game_over = False

while not game_over:
    # Gestion de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT: #Se ha de poner el "pg." delante de quit pq forma parte de la libreria pygame 
            game_over = True

    # Gestion del estado
    print("Hola mundo")
    
    #Refrescar pantalla 
    pantalla.fill((0,255,0))
    pg.display.flip()

