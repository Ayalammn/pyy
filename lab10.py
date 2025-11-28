import psycopg2
import csv
import json
import os
import sys
from random import randint
import pygame
from pygame.locals import *


DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'lab10db',        
    'user': 'postgres',          
    'password': '12345'         
}


def get_conn():
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )

def create_tables():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            phone VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS \"user\" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES \"user\"(id) ON DELETE CASCADE,
            level INTEGER NOT NULL DEFAULT 1,
            score INTEGER NOT NULL DEFAULT 0,
            state JSONB,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")


def get_user_by_username(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM \"user\" WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def create_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO \"user\" (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def save_user_score(user_id, level, score, state):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_score (user_id, level, score, state) VALUES (%s,%s,%s,%s)",
                (user_id, level, score, json.dumps(state)))
    conn.commit()
    cur.close()
    conn.close()

def insert_phonebook_console():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name,last_name,phone,email) VALUES (%s,%s,%s,%s)",
                (first_name,last_name,phone,email))
    conn.commit()
    cur.close()
    conn.close()
    print("Entry added.")

def insert_phonebook_csv():
    file_path = input("Enter CSV file path: ")
    if not os.path.exists(file_path):
        print("File does not exist.")
        return
    conn = get_conn()
    cur = conn.cursor()
    with open(file_path,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name,last_name,phone,email) VALUES (%s,%s,%s,%s)",
                        (row['first_name'],row['last_name'],row['phone'],row['email']))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted.")

def update_phonebook():
    first_name = input("Enter first name to update: ")
    new_phone = input("Enter new phone: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s", (new_phone, first_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone updated.")

def query_phonebook():
    keyword = input("Enter keyword to search in first name: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT first_name,last_name,phone,email FROM phonebook WHERE first_name ILIKE %s", (f'%{keyword}%',))
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def delete_phonebook():
    first_name = input("Enter first name to delete: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (first_name,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted.")


def run_snake_game(user_id):
    WIDTH, HEIGHT = 640, 480
    CELL_SIZE = 20
    FPS = 10

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Load saved state
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT level, score, state FROM user_score WHERE user_id=%s ORDER BY saved_at DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    if row:
        level, score, state_data = row
        if isinstance(state_data, dict):
            state = state_data
        else:
            state = json.loads(state_data)
        snake = state['snake']
        direction = state['direction']
        food = state['food']
    else:
        snake = [[WIDTH//2, HEIGHT//2]]
        direction = 'RIGHT'
        food = [CELL_SIZE*5, CELL_SIZE*5]
        score = 0
        level = 1
    cur.close()
    conn.close()

    running = True
    while running:
        clock.tick(FPS + (level-1)*2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = {'snake': snake, 'direction': direction, 'food': food}
                    save_user_score(user_id, level, score, state)
                    print("Game paused & saved.")
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        head = snake[-1].copy()
        if direction == 'UP': head[1] -= CELL_SIZE
        elif direction == 'DOWN': head[1] += CELL_SIZE
        elif direction == 'LEFT': head[0] -= CELL_SIZE
        elif direction == 'RIGHT': head[0] += CELL_SIZE
        snake.append(head)

        if head in snake[:-1] or head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT:
            print("Game Over! Score:", score)
            running = False
            continue

        if head == food:
            score += 10
            food = [CELL_SIZE*(randint(0, WIDTH//CELL_SIZE-1)), CELL_SIZE*(randint(0, HEIGHT//CELL_SIZE-1))]
        else:
            snake.pop(0)

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        font = pygame.font.SysFont(None, 24)
        img = font.render(f'Score: {score}', True, WHITE)
        screen.blit(img, (5,5))
        pygame.display.flip()

    pygame.quit()
    state = {'snake': snake, 'direction': direction, 'food': food}
    save_user_score(user_id, level, score, state)
    print("Final score saved to database.")



def run():
    while True:
        print("Lab 10 - PhoneBook and Snake Game")
        print("1) Setup database tables")
        print("2) PhoneBook: insert (console)")
        print("3) PhoneBook: insert (CSV)")
        print("4) PhoneBook: update by first name")
        print("5) PhoneBook: query (contains)")
        print("6) PhoneBook: delete by first name")
        print("7) Run Snake Game")
        print("0) Exit")
        choice = input("Choice: ")

        if choice=='1':
            create_tables()
        elif choice=='2':
            insert_phonebook_console()
        elif choice=='3':
            insert_phonebook_csv()
        elif choice=='4':
            update_phonebook()
        elif choice=='5':
            query_phonebook()
        elif choice=='6':
            delete_phonebook()
        elif choice=='7':
            username = input("Enter your username: ")
            u = get_user_by_username(username)
            if u is None:
                user_id = create_user(username)
            else:
                user_id = u[0]
            run_snake_game(user_id)
        elif choice=='0':
            print("Exiting.")
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == '__main__':
    run()

