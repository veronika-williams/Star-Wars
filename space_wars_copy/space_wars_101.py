"""
Игра Космические войны. Версия 1.0.
Завершение игры.
"""

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Параметры экрана
WIDTH = 500
HEIGHT = 600
BUTTON_WIDTH = 170
BUTTON_HEIGHT = 50
FPS = 60

add_speed = 0

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
pygame.display.set_caption("Космические войны. Версия 1.0")
clock = pygame.time.Clock()


def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont("Britannic Bold", size, True)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmeteor():
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


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
        self.shield = 100
        self.last_update = pygame.time.get_ticks()

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
        now = pygame.time.get_ticks()
        if now - self.last_update > 400:
            self.last_update = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()


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
        self.speedy = random.randrange(1, 8) + add_speed
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

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

# Загрузка изображений для взрывов
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_laser1.ogg'))
expl_sounds = []
for snd in ['sfx_shieldDown.ogg', 'sfx_shieldUp.ogg']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))


# Основной цикл игры
running = True
game_over = True
start = True

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "STAR", 65, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "WARS", 65, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Стрелки - перемещаться, Пробел - стрелять", 27,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Нажмите любую клавишу для продолжения", 22, WIDTH / 2, HEIGHT * 0.6)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(score):
    screen.blit(background, background_rect)
    draw_text(screen, "GAME", 56, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "OVER", 56, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Your Score: " + str(score), 30,
              WIDTH / 2, HEIGHT / 2)

    font = pygame.font.SysFont("Britannic Bold", 30, True)
    restart_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_button_text = font.render("Restart Game", True, WHITE)
    restart_button_text_rect = restart_button_text.get_rect(center = restart_button_rect.center)

    screen.blit(restart_button_text, restart_button_text_rect)
    pygame.draw.rect(screen, WHITE, restart_button_rect, 3)
    
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    waiting = False

while running:
    if start:
        show_go_screen()
        start = False
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmeteor()
        score = 0

    if game_over:
        show_game_over_screen(score)
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmeteor()
        score = 0

    clock.tick(FPS)

    # Рендеринг игрового поля
    screen.blit(background, background_rect)
    all_sprites.update()
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)

    # Отображение экрана
    pygame.display.flip()

    # Проверка, не ударил ли метеор игрока
    hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 3
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmeteor()
        if player.shield <= 0:
            game_over = True
            #running = False

    # Проверка, не попала ли пуля в метеор
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits:
        if (score < 500 and score + (50 - hit.radius) // 2 >= 500): 
            add_speed = 4
        elif (score < 1000 and score + (50 - hit.radius) // 2 >= 1000):
            add_speed = 7
        elif (score < 1500 and score + (50 - hit.radius) // 2 >= 1500):
            add_speed = 10
        
        score += (50 - hit.radius) // 2
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmeteor()

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
