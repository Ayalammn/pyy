import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
SPEED = 10  # Base speed


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 20)


snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake segments
direction = (CELL_SIZE, 0)  # Start moving right
level = 1
score = 0


# Each food is a dict: position, value (points), color, expiry time
foods = []

def generate_food():
    """Generate a new food in a random empty cell with random weight and lifespan."""
    while True:
        pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
               random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        if pos not in snake and all(f['pos'] != pos for f in foods):
            value = random.choice([1, 2, 3])  # Food weight: 1, 2, or 3 points
            expiry = time.time() + random.randint(5, 10)  # Disappear after 5-10 seconds
            color = RED if value == 1 else YELLOW if value == 2 else BLUE
            foods.append({'pos': pos, 'value': value, 'expiry': expiry, 'color': color})
            break

# Start with one food
generate_food()


running = True
while running:
    # Control speed based on level
    pygame.time.delay(max(10, 100 - (level * 5)))
    
  
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
    
    # ---------- Move Snake ----------
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    # Wrap around edges
    new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
    
    # Check self-collision
    if new_head in snake:
        running = False
        continue
    
    snake.insert(0, new_head)  # Move head
    
   
    eaten_food = None
    for food in foods:
        if new_head == food['pos']:
            score += food['value']  # Add food points
            eaten_food = food
            if score % 4 == 0:  # Increase level every 4 points
                level += 1
            break
    
    if eaten_food:
        foods.remove(eaten_food)
        generate_food()  # Generate new food after eating
    else:
        snake.pop()  # Remove tail if not growing
    
    # ---------- Remove Expired Food ----------
    current_time = time.time()
    foods = [f for f in foods if f['expiry'] > current_time]
    
    # Keep at least 1-2 foods on screen
    if len(foods) < 2:
        generate_food()
    
    
    screen.fill(BLACK)
    
    # Draw foods
    for food in foods:
        pygame.draw.rect(screen, food['color'], (*food['pos'], CELL_SIZE, CELL_SIZE))
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    
    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()

pygame.quit()
