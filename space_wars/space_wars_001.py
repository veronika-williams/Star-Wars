"""
Игра Космические войны. Версия 0.1.
Инициалилизация игрового поля.
"""

import pygame

# Параметры экрана
WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)

# Основное окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические войны. Версия 0.1.")
clock = pygame.time.Clock()

# Основной цикл игры
running = True
while running:

    clock.tick(FPS)

    # Рендеринг игрового поля
    screen.fill(BLACK)

    # Отображение экрана
    pygame.display.flip()

    # Отслеживание событий
    for event in pygame.event.get():

        # Выход из приложения
        if event.type == pygame.QUIT:
            running = False

# Выход из игры
pygame.quit()
