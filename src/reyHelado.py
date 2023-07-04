"""import pygame
import random
from config import *

class Fire(pygame.sprite.Sprite):
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

class ReyHelado(pygame.sprite.Sprite):
    def __init__(self, image_path: str, size: tuple, fire_image_path: str, fire_size: tuple, fire_speed: int = 5, fire_frequency: int = 60):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.fire_image_path = fire_image_path
        self.fire_size = fire_size
        self.fire_speed = fire_speed
        self.fire_frequency = fire_frequency
        self.fire_counter = 0
        self.fires = pygame.sprite.Group()

    def update(self):
        self.rect.centerx = WIDTH - self.rect.width // 2 + DESPLAZAMIENTO_DERECHA
        self.rect.centery = HEIGHT // 2 
        
        self.fire_counter += 1
        if self.fire_counter >= self.fire_frequency:
            self.fire_counter = 0
            self.lanzar_bomba()

        self.fires.update()
        self.fires.remove(*[fire for fire in self.fires if fire.rect.right < 0])

    def lanzar_bomba(self):
        cantidad_fire = CANT_FIRE  # Cantidad de bombas a lanzar

        for _ in range(cantidad_fire):
            posicion_x = self.rect.right
            posicion_y = random.randint(self.rect.top, self.rect.bottom)

            fire = Fire(self.fire_image_path, self.fire_size, self.fire_speed)
            fire.rect.midright = (posicion_x, posicion_y)
            self.fires.add(fire)"""