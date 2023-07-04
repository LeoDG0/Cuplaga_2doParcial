import pygame
from balas import Bala
from config import *

class Character(pygame.sprite.Sprite):
    def __init__(self, path_imagen: str, size: tuple, center: tuple):
        super().__init__()
        
        self.images = []  #lista de imágenes para las animaciones
        self.current_image = 1  #indice de la imagen actual
        self.load_images()
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_x = 0
        self.speed_y = 0
        self.sound_bala = pygame.mixer.Sound(SOUND_BALA)
        self.playing = True





    def load_images(self):
        
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/avionArriba.png"), SIZE_CHAR).convert_alpha())
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/idle/idle0.png"), SIZE_CHAR).convert_alpha())
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/idle/idle1.png"), SIZE_CHAR).convert_alpha())
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/idle/idle2.png"), SIZE_CHAR).convert_alpha())
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/idle/idle3.png"), SIZE_CHAR).convert_alpha())
        self.images.append(pygame.transform.scale(pygame.image.load("./src/assets/images/personaje/avionAbajo.png"), SIZE_CHAR).convert_alpha())


    def update(self):

        

        """self.current_image += 1
        if self.current_image >= 4:
            self.current_image = 1
        self.image = self.images[self.current_image]"""

        
        
        if self.current_image >= len(self.images):
            self.current_image = 1
        self.image = self.images[self.current_image]


        if self.playing:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT


#si se esta jugando se crea la instancia bala, se reproduce el sonido de disparo y se la agrega al grupo sprites para que sea dibujada en el sprites update de render
#se crea el grupo balas para la verificacion de colisiones con bombas o el jefe
    def shoot(self, sprites, balas):
        if self.playing:
            bala = Bala(BALAS_PATH, SIZE_BALAS, self.rect.midright, AMARILLO, SPEED_BULLETS)
            self.sound_bala.play()
            sprites.add(bala)
            balas.add(bala)



    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
        self.playing = False



    def reset_movement(self):
        self.speed_x = 0
        self.speed_y = 0
        self.playing = True