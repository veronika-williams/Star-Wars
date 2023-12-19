"""
Игра Космические войны. Версия 1.0.
Завершение игры.
"""

from settings import *
from meteor import Meteor
from bullet import Bullet
from explosion import Explosion


def draw_text(surf:pygame.Surface, text:str, size:int, x:float, y:float):
    """отображение текста"""

    font = pygame.font.SysFont("Britannic Bold", size, True)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmeteor():
    """создает метеор и добавляет его в группу метеоров"""

    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)


def draw_shield_bar(surf, x, y, pct):
    """отображает количество жизней"""

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


def show_go_screen():
    """показывает начальный экран"""

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
    """при завершении игры показывает счет и кнопку перезапуска игры"""

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
