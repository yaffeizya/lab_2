#Imports
import pygame as p
import random, time
import psycopg2

# Current user name
current_user = ''

# Database connection setup
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="1488",
    port="5432"
)

#  Create "users" table
query_create_table_users = """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE
    )
"""

# Create "user_scores" table
query_create_table_user_scores = """
    CREATE TABLE IF NOT EXISTS user_scores(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        score INTEGER,
        level INTEGER
    )
"""

# Execute a SQL query
def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print( error)

# Input user name
def input_user():
    global current_user
    current_user = input("Enter your username: ")

# Add new user to the database
def add_user(name):
    command = "INSERT INTO users(username) VALUES(%s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print("add_user:", error)

# Check if a user already exists
def check_if_user_exists(name):
    command = "SELECT username FROM users WHERE username = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            result = cur.fetchall()
            return bool(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print("check_if_user_exists:", error)

# Insert new score
def add_new_score(score, lvl):
    command = "INSERT INTO user_scores(username, score, level) VALUES(%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user, score, lvl))
            conn.commit()
            print(f" Score saved: {current_user}, Score: {score}, Level: {lvl}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(" add_new_score:", error)

# Save game score
def process_score(score, lvl):
    print(f" Saving: {score}, level: {lvl}, user: {current_user}")
    user_exists = check_if_user_exists(current_user)
    if not user_exists:
        print(" User not found")
        add_user(current_user)
    add_new_score(score, lvl)

# Show user's highest level
def show_highest_level():
    command = "SELECT MAX(level) FROM user_scores WHERE username = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            result = cur.fetchall()
            return result
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    execute_query(query_create_table_users)
    execute_query(query_create_table_user_scores)
# Initialize pygame
p.init()
clock = p.time.Clock()

# Game screen setup
X, Y = 800, 800
block = 20
screen = p.display.set_mode((X, Y))
p.display.set_caption("Snake")

# Background
back = p.image.load("/Users/mukhametaliissayev/Downloads/snake_fon.jpg")
back = p.transform.scale(back, (800, 800))

# Snake initial state
snake_head = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
snake_dir = "RIGHT"
change_to = snake_dir

# Food setup
food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
food = p.image.load("/Users/mukhametaliissayev/Downloads/apple.png")
food1 = p.transform.scale(food, (40, 40))
food_size1 = p.transform.scale(food, (10, 10))
food_size2 = p.transform.scale(food, (20, 20))
food_size3 = p.transform.scale(food, (30, 30))
food_size = [food_size1, food_size2, food_size3]
food = food_size3
food_active = True
food_spawn_time = time.time()

# Fonts
font = p.font.SysFont("Arial", 40)
font_big = p.font.SysFont("Sand", 70)
game_over = font_big.render("Game Over", True, (0, 0, 0))

# Buttons
qquit = p.image.load("/Users/mukhametaliissayev/Downloads/quit.png")
qquit = p.transform.scale(qquit, (125, 102))
restart = p.image.load("/Users/mukhametaliissayev/Downloads/restart.png")
restart = p.transform.scale(restart, (125, 90))

# Game variables
SPEED = 5
score = 0
level = 1
prev_level = 1
collision = False
run = True

# Get username
input_user()

# Main game loop
while run:
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

        if event.type == p.KEYDOWN and not collision:
            if event.key == p.K_UP and snake_dir != "DOWN":
                change_to = "UP"
            elif event.key == p.K_DOWN and snake_dir != "UP":
                change_to = "DOWN"
            elif event.key == p.K_LEFT and snake_dir != "RIGHT":
                change_to = "LEFT"
            elif event.key == p.K_RIGHT and snake_dir != "LEFT":
                change_to = "RIGHT"

        if event.type == p.MOUSEBUTTONDOWN and collision:
            mouse_pos = p.mouse.get_pos()
            restart_rect = restart.get_rect(topleft=(250, 373))
            qquit_rect = qquit.get_rect(topleft=(450, 367))

            if restart_rect.collidepoint(mouse_pos):
                time.sleep(0.5)
                # Reset game
                score = 0
                SPEED = 5
                level = 1
                snake_head = [100, 50]
                snake_body = [[100, 50], [80, 50], [60, 50]]
                snake_dir = "RIGHT"
                change_to = snake_dir
                collision = False

            elif qquit_rect.collidepoint(mouse_pos):
                time.sleep(0.5)
                run = False

    # Food timeout logic
    if food_active and (time.time() - food_spawn_time >= 4):
        food_active = False
        food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
        food = random.choice(food_size)
        food_active = True
        food_spawn_time = time.time()

    # Update snake direction
    snake_dir = change_to
    if snake_dir == "UP":
        snake_head[1] -= SPEED
    elif snake_dir == "DOWN":
        snake_head[1] += SPEED
    elif snake_dir == "LEFT":
        snake_head[0] -= SPEED
    elif snake_dir == "RIGHT":
        snake_head[0] += SPEED

    # Move snake
    snake_body.insert(0, list(snake_head))

    # Check for wall collision
    if snake_head[0] <= 0 or snake_head[0] >= X or snake_head[1] <= 0 or snake_head[1] >= Y:
        collision = True
        process_score(score, level)

    # Check for self collision
    for segment in snake_body[1:]:
        if snake_head == segment:
            collision = True
            process_score(score, level)

    # Check if food is eaten
    if (food_pos[0] - 15 <= snake_head[0] <= food_pos[0] + 25 and
        food_pos[1] - 15 <= snake_head[1] <= food_pos[1] + 25):
        food_spawn_time = time.time()
        if food == food_size1:
            score += 3
        elif food == food_size2:
            score += 2
        elif food == food_size3:
            score += 1
        food = random.choice(food_size)
        food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
        snake_body.append(snake_body[-1])
        SPEED = 5 + (score // 5)
        level = 1 + (score // 5)
        if level > prev_level:
            prev_level = level
    else:
        snake_body.pop()

    # Drawing
    screen.blit(back, (0, 0))
    if not collision:
        for segment in snake_body:
            p.draw.rect(screen, (255, 255, 255), p.Rect(segment[0], segment[1], block, block))
        if food_active:
            screen.blit(food, food_pos)
        scores = font.render(str(score), True, (0, 0, 0))
        levels = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(levels, (350, 20))
        screen.blit(food1, (X - 88, 23))
        screen.blit(scores, (X - 40, 20))
    else:
        screen.blit(game_over, (280, 200))
        screen.blit(restart, (250, 373))
        screen.blit(qquit, (450, 367))
        scores = font.render(str(score), True, (0, 0, 0))
        screen.blit(food1, (X - 88, 23))
        screen.blit(scores, (X - 40, 20))

    p.display.update()
    clock.tick(60)