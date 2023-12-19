
import pygame
import random
from os import path

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


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


# Загрузка игровой графики
background = pygame.image.load(path.join(img_dir, "purple.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()

# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_laser1.ogg'))
expl_sounds = []
for snd in ['sfx_shieldDown.ogg', 'sfx_shieldUp.ogg']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# Основной цикл игры
running = True
game_over = True
start = True