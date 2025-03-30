import pygame
import random

SCREEN = WIDTH, HEIGHT = 750, 600
lan_pos = [100, 250, 400, 550]

class Player:
    def __init__(self, x, y, type):
        self.image = pygame.image.load(f'data/Assets/cars/{type+1}.png')
        self.image = pygame.transform.scale(self.image, (82, 116))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = False

    def update(self, left, right):
        if left:
            self.rect.x -= 5
            if self.rect.x <= 50:
                self.rect.x = 50
        if right:
            self.rect.x += 5
            if self.rect.right >= WIDTH - 50:
                self.rect.right = WIDTH - 50

    def draw(self, win):
        if self.visible:
            win.blit(self.image, self.rect)

class Road:
    def __init__(self):
        self.image = pygame.image.load('data/Assets/road.png')
        self.image = pygame.transform.scale(self.image, (WIDTH - 60, HEIGHT))
        self.move = True
        self.reset()

    def reset(self):
        self.x = 30
        self.y1 = 0
        self.y2 = -HEIGHT

    def update(self, speed):
        if self.move:
            self.y1 += speed
            self.y2 += speed
        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT

    def draw(self, win):
        win.blit(self.image, (self.x, self.y1))
        win.blit(self.image, (self.x, self.y2))

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tree, self).__init__()
        type = random.randint(1, 4)
        self.image = pygame.image.load(f'data/Assets/trees/{type}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        self.rect.y += speed
        if self.rect.y >= HEIGHT:
            self.kill()

    def draw(self, win):
        win.blit(self.image, self.rect)

class Pr(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Pr, self).__init__()
        self.type = type
        dx = 0

        if type == 1:
            ctype = random.randint(2, 8)
            self.image = pygame.image.load(f'data/Assets/cars/{ctype}.png')
            self.image = pygame.transform.flip(self.image, False, True)
            self.image = pygame.transform.scale(self.image, (82, 116))
            self.min_gap = 200
        elif type == 2:
            self.image = pygame.image.load('data/Assets/barrel.png')
            self.image = pygame.transform.scale(self.image, (40, 60))
            dx = 10
            self.min_gap = 150
        elif type == 3:
            self.image = pygame.image.load('data/Assets/roadblock.png')
            self.image = pygame.transform.scale(self.image, (100, 50))
            self.min_gap = 300

        self.rect = self.image.get_rect()
        self.rect.x = random.choice(lan_pos) + dx
        self.rect.y = -self.min_gap

    def update(self, speed):
        self.rect.y += speed
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect)