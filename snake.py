import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
SPEED = 10

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 20)

# Змейка и еда
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
level, score = 1, 0

# Генерация еды в безопасном месте
def generate_food():
    while True:
        food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        if food not in snake:
            return food

food = generate_food()

# Игровой цикл
running = True
while running:
    pygame.time.delay(100 - (level * 5))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
        direction = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
        direction = (CELL_SIZE, 0)
    if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
        direction = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
        direction = (0, CELL_SIZE)
    
    # Движение змейки
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Проверка на столкновение с границей (змейка выходит с другой стороны)
    if new_head[0] < 0:
        new_head = (WIDTH - CELL_SIZE, new_head[1])
    elif new_head[0] >= WIDTH:
        new_head = (0, new_head[1])
    if new_head[1] < 0:
        new_head = (new_head[0], HEIGHT - CELL_SIZE)
    elif new_head[1] >= HEIGHT:
        new_head = (new_head[0], 0)
    
    # Проверка на столкновение с собой
    if new_head in snake:
        running = False
        continue
    
    snake.insert(0, new_head)
    
    # Проверка на съедение еды
    if new_head == food:
        score += 1
        food = generate_food()
        if score % 4 == 0:
            level += 1  # Повышение уровня каждые 4 еды
    else:
        snake.pop()
    
    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    
    # Отображение счёта и уровня
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()
    
pygame.quit()
