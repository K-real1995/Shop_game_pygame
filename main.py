from random import randint
import pygame
from ball import Ball

# Устанавливаем значения музыки, окна, генерации элементов, фона
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)
# Фоновая музыка
pygame.mixer.music.load('music/music.mp3')
pygame.mixer.music.play(-1)
# Эффект при ловле продукта
s_catch = pygame.mixer.Sound("music/hit.wav")

BLACK = (0, 0, 0)
W, H = 600, 400

sc = pygame.display.set_mode((600, 400))

clock = pygame.time.Clock()
FPS = 60
# Фон и шрифт очков
score = pygame.image.load('images/score.png').convert_alpha()
fnt = pygame.font.SysFont("arial", 30)
# Тележка и положение тележки
cart = pygame.image.load("images/cart.png").convert_alpha()
t_rect = cart.get_rect(centerx=W // 2, bottom=H - 5)
# Cписок изображений продуктов вызываемых случайным образом
balls_data = ({"path": "bigmac.png", "score": 100},
              {"path": "pringles.png", "score": 150},
              {"path": "sprite_can.png", "score": 200},
              {"path": "choco_pie.png", "score": 250},
              {"path": "beer.png", "score": 300},
              {"path": "pizza.png", "score": 350})
balls_surf = [pygame.image.load('images/' + data["path"]).convert_alpha() for data in balls_data]


# Функция рандомного создания продуктов
def create_ball(group) -> Ball:
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Ball(x, speed, balls_surf[indx], balls_data[indx]["score"], group)


# Начальное количество очков
game_score = 0


# Функция начисляющая очки воспроизводящая звуковой эффект и уничтожающая продукт при стоклновении с тележкой
def collide_balls() -> None:
    global game_score
    for ball in balls:
        if t_rect.collidepoint(ball.rect.center):
            s_catch.play()
            game_score += ball.score
            ball.kill()


balls = pygame.sprite.Group()

bg = pygame.image.load('images/background.bmp').convert()

speed = 10
create_ball(balls)
# Главный цикл программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            create_ball(balls)
    # Реагирование тележки на нажатие клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        t_rect.x += speed
        if t_rect.x > W - t_rect.width:
            t_rect.x = W - t_rect.width

    collide_balls()

    sc.blit(bg, (0, 0))
    sc.blit(score, (0, 0))
    sc_text = fnt.render(str(game_score), True, BLACK)
    sc.blit(sc_text, (20, 10))
    balls.draw(sc)
    sc.blit(cart, t_rect)
    pygame.display.update()

    clock.tick(FPS)

    balls.update(H)
