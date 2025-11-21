
import pygame, sys
from pygame.locals import *
import random

pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")


SPEED = 3  # Enemy speed
SCORE = 0  # Points for dodging cars
COINS = 0  # Total coins collected


font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)


background = pygame.image.load("/Users/ayalatileuzhan/Downloads/AnimatedStreet.png")
background_y = 0  # For scrolling background


class Enemy(pygame.sprite.Sprite):
    """Enemy cars moving down the screen"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ayalatileuzhan/Downloads/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move enemy down and respawn if off-screen"""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    """Coins with random weights"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ayalatileuzhan/Downloads/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.randomize_position()
        self.value = random.choice([1, 2, 3])  # Coin weight

    def randomize_position(self):
        """Randomly place coin on the screen"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40),
                            random.randint(-200, SCREEN_HEIGHT - 40))

    def move(self):
        """Move coin down and handle collision with player"""
        global COINS, SPEED  # Declare globals at top
        self.rect.move_ip(0, SPEED)

        # If off-screen, respawn
        if self.rect.top > SCREEN_HEIGHT:
            self.randomize_position()
            self.value = random.choice([1, 2, 3])

        # Collision with player
        if pygame.sprite.collide_rect(self, P1):
            COINS += self.value  # Add coin weight
            self.randomize_position()
            self.value = random.choice([1, 2, 3])

            # Increase speed every 10 coins
            if COINS % 10 == 0:
                SPEED += 1


class Player(pygame.sprite.Sprite):
    """Player car controlled by arrow keys"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ayalatileuzhan/Downloads/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """Move player based on pressed keys"""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)



P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Increase speed gradually


def game_over_screen():
    """Display Game Over screen"""
    screen.fill(RED)
    screen.blit(game_over_text, (30, 250))
    pygame.display.update()
    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # Restart game
                    return True
                elif event.key == K_ESCAPE:  # Exit game
                    return False


while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1  # Gradually increase speed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Check collision with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        if not game_over_screen():  # If player chooses to exit
            pygame.quit()
            sys.exit()

    # Scroll background
    background_y = (background_y + SPEED) % background.get_height()
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_height()))

    # Display score and coins
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    screen.blit(score_text, (10, 10))
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    screen.blit(coins_text, (270, 10))

    # Move and draw all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if entity == C1:
            entity.move()  # Move coin and handle collection
        elif entity == E1:
            entity.move()  # Move enemy
        elif entity == P1:
            entity.move()  # Move player

    pygame.display.update()
    FramePerSec.tick(FPS)
