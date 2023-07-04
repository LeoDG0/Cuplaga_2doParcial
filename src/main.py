import pygame
import sys

from config import *
from character import Character
from carnation import Diablo
from balas import Bala

import random

pygame.init()
pygame.display.set_caption("CupLaga")



reloj = pygame.time.Clock()
#sonido = pygame.mixer.Sound("./src/assets/sound/disparo.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 255, 0))

fondo = pygame.image.load("./src/assets/fondos/fondoPaisaje.jpg").convert()
fondo = pygame.transform.scale(fondo, SCREEN_SIZE)

diablo = Diablo(DIABLO_PATH, SIZE_DIABLO, BOMBA_PATH, SIZE_BOMBA, SPEED_BOMBA, BOMB_FRECUENCY)

avion = Character(CHAR_PATH, SIZE_CHAR, START_POS)

sprites = pygame.sprite.Group()
balas = pygame.sprite.Group()

sprites.add(avion) 
sprites.add(diablo)




nivel_actual = 1
nivel_completado = False

golpes_character = 0
balas_recibidas_jefe = 0


while True:
    reloj.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                avion.speed_x = -SPEED_CHAR

            if event.key == pygame.K_RIGHT:
                avion.speed_x = SPEED_CHAR

            if event.key == pygame.K_UP:
                avion.speed_y = -SPEED_CHAR

            if event.key == pygame.K_DOWN:
                avion.speed_y = SPEED_CHAR

            if event.key == pygame.K_SPACE:
                avion.shoot(sprites, balas)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and avion.speed_x < 0:
                avion.speed_x = 0
            if event.key == pygame.K_RIGHT and avion.speed_x > 0:
                avion.speed_x = 0

            if event.key == pygame.K_UP and avion.speed_y < 0:
                avion.speed_y = 0

            if event.key == pygame.K_DOWN and avion.speed_y > 0:
                avion.speed_y = 0
        
            if avion.rect.left <= 0:
                avion.rect.left = 0
            if avion.rect.right >= WIDTH:
                avion.rect.right = WIDTH
            if avion.rect.top <= 0:
                avion.rect.top = 0
            if avion.rect.bottom >= HEIGHT:
                avion.rect.bottom = HEIGHT

    if nivel_actual == 1:

        # Verificar colisiones entre balas del character y bombas del jefe
        for bala in balas:
            impactos = pygame.sprite.spritecollide(bala, diablo.bombs, True)
            if impactos:
                balas_recibidas_jefe += len(impactos)
                bala.kill()

        # Verificar colisiones entre balas del personaje y jefe
        for bala in balas:
            if bala.rect.colliderect(diablo.rect):
                balas_recibidas_jefe  += 1
                bala.kill()

        #golpes recibidos por el jefe
        for bomba in diablo.bombs:
            if bomba.rect.colliderect(avion.rect):
                bomba.kill()
                golpes_character += 1
                break

        # Verificar condiciones de derrota o victoria
        if golpes_character >= 3:
            # Derrota del character
            break

        if balas_recibidas_jefe >= 10:
            nivel_completado = True # Derrota del jefe 

        if nivel_completado:
            break  

    if nivel_actual == 2:
        pass
        

    # Actualizar personajes y elementos del nivel
    sprites.update()
    diablo.update()
    balas.update()
    diablo.bombs.update()

    screen.blit(fondo, ORIGIN)
    sprites.draw(screen)
    diablo.bombs.draw(screen)
    pygame.display.flip()