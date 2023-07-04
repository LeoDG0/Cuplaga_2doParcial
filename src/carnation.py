import pygame
import random
from config import *
from sprites import *


class Carnation(pygame.sprite.Sprite):
    def __init__(self, animations: str, size: tuple, bomb_image_path: str, bomb_size: tuple, bomb_speed: int = 5, bomb_frequency: int = 60):
        super().__init__()

        self.animations = animations
        self.current_image = 0
        self.animation_speed = 10
        self.animation_counter = 0

        self.image = self.animations[self.current_image]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = WIDTH - self.rect.width // 2 + DESPLAZAMIENTO_DERECHA
        self.rect.centery = HEIGHT // 2 
        
        self.bomb_image_path = bomb_image_path
        self.bomb_size = bomb_size
        self.bomb_speed = bomb_speed
        self.bomb_frequency = bomb_frequency
        self.bomb_counter = 0
        self.bombs_cant = CANT_BOMBA
        self.bombs = pygame.sprite.Group()


#controla la ubicacion del jefe y el desplazamiento derecha es para moverlo hacia la derecha
#
    def update(self):
        #carnation
        self.rect.centerx = WIDTH - self.rect.width // 2 + DESPLAZAMIENTO_DERECHA
        self.rect.centery = HEIGHT // 2 
        self.mask = pygame.mask.from_surface(self.image) #mascara para que la colision sea con la imagen y no el cuadrado


        self.bomb_counter += 1 #contador de bombas
        if self.bomb_counter >= self.bomb_frequency: #verifica que el contador no supere la frecuencia
            self.bomb_counter = 0 #reinciar el contador
            self.lanzar_bomba() #generar una nueva bomba

        self.bombs.update() #actualiza todas las bombas
        self.bombs.remove(*[bomba for bomba in self.bombs if bomba.rect.right < 0]) #se crea una lista con las bombas que salen de la pantalla y con remove se las elimina
        
        self.animate()



    def animate(self):
        self.animation_counter += 1 
        if self.animation_counter >= self.animation_speed: 
            self.animation_counter = 0
            self.current_image += 1
            if self.current_image >= len(self.animations):
                self.current_image = 0
        self.image = self.animations[self.current_image]


#recibe la cantidad de bombas a lanzar, en el for se ejecuta en base a la cant de bombas
#se calcula donde se van a spawnear osea x y con random se crean diferentes posiciones en y
#crea una instancia de Bomba y se la posiciona en el centro del rectangulo de la bomba
#y se crea una mascara para que la colision sea con la mascara en vez del caudrado y se agrega al grupo bomba
    def lanzar_bomba(self):
        cantidad_bombas = self.bombs_cant  #Cantidad de bombas a lanzar

        for _ in range(cantidad_bombas):
            posicion_x = self.rect.right
            posicion_y = random.randint(self.rect.top, self.rect.bottom)

            bomba = Bomba(self.bomb_image_path, self.bomb_size, self.bomb_speed)
            bomba.rect.midright = (posicion_x, posicion_y)
            
            bomba.mask = pygame.mask.from_surface(bomba.image)
            
            self.bombs.add(bomba)    



    
    def stop(self):
        self.bomb_frequency = 0
        self.bombs_cant = 0
        self.bomb_speed = 0
    



    def reset_bombs(self):
        self.bombs.empty()
        self.bomb_frequency = BOMB_FRECUENCY
        self.bombs_cant = CANT_BOMBA
        self.bomb_speed = SPEED_BOMBA


class Bomba(pygame.sprite.Sprite):
    
    def __init__(self, image_path: str, size: tuple, speed: int = 5):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.speed = speed



    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()