import pygame
import random

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")
screen.fill(WHITE)

# Переменные состояния
painting = False
last_pos = None
color = BLACK
mode = "pen"  # pen, rect, circle, eraser
start_pos = None
eraser_size = 10  # Начальный размер ластика

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                painting = True
                last_pos = event.pos
                start_pos = event.pos
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка мыши
                painting = False
                if mode == "rect":
                    end_pos = event.pos
                    pygame.draw.rect(screen, color, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), 2)
                elif mode == "circle":
                    end_pos = event.pos
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)
            
        elif event.type == pygame.MOUSEMOTION:
            if painting:
                if mode == "pen":
                    pygame.draw.line(screen, color, last_pos, event.pos, 3)
                    last_pos = event.pos
                elif mode == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, eraser_size)
                    last_pos = event.pos
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_p:
                mode = "pen"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_1:
                color = (255, 0, 0)  # Красный
            elif event.key == pygame.K_2:
                color = (0, 255, 0)  # Зеленый
            elif event.key == pygame.K_3:
                color = (0, 0, 255)  # Синий
            elif event.key == pygame.K_4:
                color = BLACK  # Черный
            elif event.key == pygame.K_LEFTBRACKET:  # Клавиша [
                eraser_size = max(5, eraser_size - 5)  # Минимум 5 пикселей
            elif event.key == pygame.K_RIGHTBRACKET:  # Клавиша ]
                eraser_size += 5  # Увеличиваем размер
    
    pygame.display.flip()
    
pygame.quit()
