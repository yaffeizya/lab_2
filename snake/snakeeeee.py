# Imports
import pygame as p
import random, time
import psycopg2

# Connect with database
connect = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="1488",
    port="5432"
)
cursor = connect.cursor()

#Creating db
cursor.execute("""
    CREATE TABLE IF NOT EXISTS snake_scores (
        id SERIAL PRIMARY KEY,
        player_name VARCHAR(50),
        score INT
    )
""")
connect.commit()

# Initializing
p.init()

# Setting up FPS
clock = p.time.Clock()

# Create a screen
X = 800
Y = 800
block = 20
screen = p.display.set_mode((X, Y))
p.display.set_caption("Snake")
back = p.image.load("/Users/mukhametaliissayev/Downloads/snake_fon.jpg")
back = p.transform.scale(back, (800, 800))

# Creating a snake
snake_head = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
snake_dir = "RIGHT"
change_to = snake_dir

# Creating an apple
food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
food = p.image.load("/Users/mukhametaliissayev/Downloads/apple.png")
food = p.transform.scale(food, (30, 30))
food1 = p.transform.scale(food, (40, 40))
food_size1 = p.transform.scale(food, (10, 10))
food_size2 = p.transform.scale(food, (20, 20))
food_size3 = p.transform.scale(food, (30, 30))
food_size = [food_size1, food_size2, food_size3]
food = food_size3
food_active = True
food_spawn_time = time.time()

# Setting up fonts
font = p.font.SysFont("Arial", 40)
font2 = p.font.SysFont("Sand", 40)
font_big = p.font.SysFont("Sand", 70)
game_over = font_big.render("Game Over", True, (0, 0, 0))

# Setting up buttons
qquit = p.image.load("/Users/mukhametaliissayev/Downloads/quit.png")
qquit = p.transform.scale(qquit, (125, 102))
restart = p.image.load("/Users/mukhametaliissayev/Downloads/restart.png")
restart = p.transform.scale(restart, (125, 90))

# Other variables for program
SPEED = 5
score = 0
level = 1
prev_level = 1
hit_sound = False
collision = True
run = True
start_screen = True
player_name = ""
player_score = 0
pause = False

#input name
name_input = ""
input_active = True

#walls
wall1 = (200,200)
wall2 = (400,400)
wall3 = (600,600)

while run:
    if start_screen:
        #draw starting screen
        screen.blit(back, (0, 0))
        prompt = font2.render("Enter your name:", True, (0, 0, 0))
        name_text = font2.render(name_input, True, (0, 0, 0))
        
        # max score
        cursor.execute("SELECT MAX(score) FROM snake_scores WHERE player_name = %s", (name_input.strip(),))
        max_score = cursor.fetchone()[0]
        if max_score is None:
            max_score = 0
        score_text = font2.render(f"Max Score: {max_score}", True, (0, 0, 0))
        
        screen.blit(prompt, (300, 300))
        screen.blit(name_text, (300, 350))
        screen.blit(score_text, (300, 400))  
        p.draw.rect(screen, (0, 0, 0), (295, 340, 200, 40), 2)  
        p.display.update()

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            elif event.type == p.KEYDOWN and input_active:
                if event.key == p.K_RETURN and name_input.strip() != "":
                    player_name = name_input.strip()
                    start_screen = False
                    collision = False
                elif event.key == p.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif len(name_input) < 20:
                    name_input += event.unicode
    else:
        # main loop
        for i in p.event.get():
            if i.type == p.QUIT:
                run = False
            if i.type == p.KEYDOWN:
                if i.key == p.K_ESCAPE and not collision:
                    pause = not pause
                if not collision and not pause:
                    if i.key == p.K_UP and snake_dir != "DOWN":
                        change_to = "UP"
                    if i.key == p.K_DOWN and snake_dir != "UP":
                        change_to = "DOWN"
                    if i.key == p.K_LEFT and snake_dir != "RIGHT":
                        change_to = "LEFT"
                    if i.key == p.K_RIGHT and snake_dir != "LEFT":
                        change_to = "RIGHT"
                    if i.key == p.K_SPACE:
                        cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                        )
                        connect.commit()

            if i.type == p.MOUSEBUTTONDOWN and collision:
                mouse_pos = p.mouse.get_pos()
                restart_rect = restart.get_rect(topleft=(250, 373))
                if restart_rect.collidepoint(mouse_pos):
                    time.sleep(0.5)
                    score = 0
                    SPEED = 5
                    level = 1
                    snake_head = [100, 50]
                    snake_body = [[100, 50], [80, 50], [60, 50]]
                    snake_dir = "RIGHT"
                    change_to = snake_dir
                    collision = False
                    hit_sound = False
                    start_screen = True  
                    name_input = ""     
                    player_name = ""    
                    pause = False
                qquit_rect = qquit.get_rect(topleft=(450, 367))
                if qquit_rect.collidepoint(mouse_pos):
                    time.sleep(0.5)
                    run = False

        if not collision and not pause:
            if food_active and (time.time() - food_spawn_time >= 4):
                food_active = False
                food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall1[0] and food_pos[0] < wall1[0]+block and food_pos[1] > wall1[1] and food_pos[1] < wall1[1]+100:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall2[0] and food_pos[0] < wall2[0]+100 and food_pos[1] > wall2[1] and food_pos[1] < wall2[1]+block:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall3[0] and food_pos[0] < wall3[0]+block and food_pos[1] > wall3[1] and food_pos[1] < wall3[1]+100:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                food_active = True
                food_spawn_time = time.time()

            # Changing snake
            snake_dir = change_to
            if snake_dir == "UP" and not pause:
                snake_head[1] -= SPEED
            elif snake_dir == "DOWN" and not pause:
                snake_head[1] += SPEED
            elif snake_dir == "LEFT" and not pause:
                snake_head[0] -= SPEED
            elif snake_dir == "RIGHT" and not pause:
                snake_head[0] += SPEED

            snake_body.insert(0, list(snake_head))

            # Checking for collisions
            if (
                snake_head[0] <= 0
                or snake_head[0] >= X
                or snake_head[1] <= 0
                or snake_head[1] >= Y
            ):
                collision = True
                if not hit_sound:
                    hit_sound = True
                    cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                    )
                    connect.commit()

            for i in snake_body[1:]:
                if snake_head == i:
                    collision = True
                    if not hit_sound:
                        hit_sound = True
                    cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                    )
                    connect.commit()
            if level >= 2 and snake_head[0] > wall1[0] and snake_head[0] < wall1[0]+block and snake_head[1] > wall1[1] and snake_head[1] < wall1[1]+100:
                 collision = True
                 if not hit_sound:
                    hit_sound = True
                    cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                    )
                    connect.commit()
            if level >= 3 and snake_head[0] > wall2[0] and snake_head[0] < wall2[0]+100 and snake_head[1] > wall2[1] and snake_head[1] < wall2[1]+block:
                 collision = True
                 if not hit_sound:
                    hit_sound = True
                    cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                    )
                    connect.commit()
            if level >= 4 and snake_head[0] > wall3[0] and snake_head[0] < wall3[0]+block and snake_head[1] > wall3[1] and snake_head[1] < wall3[1]+100:
                 collision = True
                 if not hit_sound:
                    hit_sound = True
                    cursor.execute(
                        "INSERT INTO snake_scores (player_name, score) VALUES (%s, %s)",
                        (player_name, score)
                    )
                    connect.commit()


            # Collecting apples
            if (
                snake_head[0] >= food_pos[0] - 15
                and snake_head[0] <= food_pos[0] + 25
                and snake_head[1] >= food_pos[1] - 15
                and snake_head[1] <= food_pos[1] + 25
            ):
                food_spawn_time = time.time()
                if food == food_size1:
                    score += 3
                elif food == food_size2:
                    score += 2
                elif food == food_size3:
                    score += 1
                if score > max_score:
                    score_text = font2.render(f"Max Score: {max_score}", True, (0, 0, 0))
                food = random.choice(food_size)
                food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall1[0] and food_pos[0] < wall1[0]+block and food_pos[1] > wall1[1] and food_pos[1] < wall1[1]+100:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall2[0] and food_pos[0] < wall2[0]+100 and food_pos[1] > wall2[1] and food_pos[1] < wall2[1]+block:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                if food_pos[0] > wall3[0] and food_pos[0] < wall3[0]+block and food_pos[1] > wall3[1] and food_pos[1] < wall3[1]+100:
                    food_pos = [random.randint(block, X - block), random.randint(block, Y - block)]
                snake_body.append(list(snake_body[-1]))
                SPEED = 5 + (score // 5)
                level = 1 + (score // 5)
                if level - prev_level >= 1:
                    prev_level = level
            else:
                snake_body.pop()

        # Display before and after
        if not collision:
            screen.blit(back, (0, 0))
            for i in snake_body:
                p.draw.rect(screen, (255, 255, 255), p.Rect(i[0], i[1], block, block))
            if food_active:
                screen.blit(food, food_pos)
            scores = font.render(str(score), True, (0, 0, 0))
            levels = font.render(f"Level:{level}", True, (0, 0, 0))
            name_display = font2.render(f"Player: {player_name}", True, (0, 0, 0))
            screen.blit(name_display, (20, 20))
            screen.blit(levels, (350, 20))
            screen.blit(food1, (X - 88, 23))
            screen.blit(scores, (X - 40, 20))
            if score < max_score:
                screen.blit(score_text, (20, 50))
            else:
                cur_score_text = font2.render(f"Max Score: {score}", True, (0, 0, 0))
                screen.blit(cur_score_text, (20, 50))
            if score >= 10:
                p.draw.rect(screen, (0, 0, 0), p.Rect(X - 90, 24, 90, 40), 2)
            else:
                p.draw.rect(screen, (0, 0, 0), p.Rect(X - 90, 24, 75, 40), 2)
            if pause:
                p.draw.line(screen, (0, 0, 0), (370, 360),(370, 440), 15)
                p.draw.line(screen, (0, 0, 0), (430, 360),(430, 440), 15)
            if level >= 2:
                p.draw.rect(screen, (128, 128, 128), p.Rect(wall1[0], wall1[1], block, 100))
            if level >= 3:
                p.draw.rect(screen, (128, 128, 128), p.Rect(wall2[0], wall2[1], 100, block))
            if level >= 4:
                p.draw.rect(screen, (128, 128, 128), p.Rect(wall3[0], wall3[1], block, 100))
        else:
            screen.blit(back, (0, 0))
            screen.blit(game_over, (280, 200))
            screen.blit(restart, (250, 373))
            screen.blit(qquit, (450, 367))
            screen.blit(food1, (X - 88, 23))
            screen.blit(scores, (X - 40, 20))
            name_display = font2.render(f"Player: {player_name}", True, (0, 0, 0))
            screen.blit(name_display, (20, 20))
            if score < max_score:
                screen.blit(score_text, (20, 50))
            else:
                cur_score_text = font2.render(f"Max Score: {score}", True, (0, 0, 0))
                screen.blit(cur_score_text, (20, 50))
            if score >= 10:
                p.draw.rect(screen, (0, 0, 0), p.Rect(X - 90, 24, 90, 40), 2)
            else:
                p.draw.rect(screen, (0, 0, 0), p.Rect(X - 90, 24, 75, 40), 2)
            p.display.update()

        p.display.update()
        clock.tick(60)


cursor.close()
connect.close()