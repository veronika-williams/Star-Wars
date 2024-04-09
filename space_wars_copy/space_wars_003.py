"""
Игра Космические войны. Версия 0.3.
Cпрайты метеоров.
"""

import pygame
import random

# Параметры экрана
WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Основное окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические войны. Версия 0.3.")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            # если улетел за пределы то возвращаем в начало
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

meteors = pygame.sprite.Group()
for i in range(8):
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)

# Основной цикл игры
running = True
while running:

    clock.tick(FPS)

    # Рендеринг игрового поля
    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)

    # Отображение экрана
    pygame.display.flip()

    # Отслеживание событий
    for event in pygame.event.get():

        # Выход из приложения
        if event.type == pygame.QUIT:
            running = False

# Выход из игры
pygame.quit()
