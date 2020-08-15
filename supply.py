import pygame
from random import *


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        randint(0, self.width - self.rect.width), -100
        self.speed = 5
        self.alive = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.alive = False

    def reset(self):
        self.alive = True
        self.rect.left, self.rect.bottom = \
                        randint(0, self.width - self.rect.width), -100


class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        randint(0, self.width - self.rect.width), -100
        self.speed = 5
        self.alive = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.alive = False

    def reset(self):
        self.alive = True
        self.rect.left, self.rect.bottom = \
                        randint(0, self.width - self.rect.width), -100
