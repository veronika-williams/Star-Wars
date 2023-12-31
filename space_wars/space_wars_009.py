"""
Игра Космические войны. Версия 0.9.
Подсчет очков за уничтоженные метеоры.
"""

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

# Параметры экрана
WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Основное окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические войны. Версия 0.9")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # уничтожить пулю за пределами экрана
        if self.rect.bottom < 0:
            self.kill()


# Загрузка игровой графики
background = pygame.image.load(path.join(img_dir, "purple.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png', 
               'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

meteors = pygame.sprite.Group()
for i in range(8):
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)

bullets = pygame.sprite.Group()

score = 0

# Основной цикл игры
running = True
while running:

    clock.tick(FPS)

    # Рендеринг игрового поля
    screen.blit(background, background_rect)
    all_sprites.update()
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    # Отображение экрана
    pygame.display.flip()

    # Проверка, не ударил ли метеор игрока
    hits = pygame.sprite.spritecollide(player, meteors, False)
    if hits:
        running = False

    # Проверка, не попала ли пуля в метеор
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        m = Meteor()
        all_sprites.add(m)
        meteors.add(m)

    # Отслеживание событий
    for event in pygame.event.get():

        # Выход из приложения
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

# Выход из игры
pygame.quit()
