import pygame
from config import *

class Bala(pygame.sprite.Sprite):
    def __init__(self, image_path: str ,size: tuple, midright: tuple, color: tuple = (255, 0, 0),speed: int = 10):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.midright = midright
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
    
    def stop(self):
        self.speed = 0
