#Imports
import pygame as p
import random, time

#Initialzing 
p.init()

#Setting up FPS
clock = p.time.Clock()

#Create a screen
X = 800
Y = 800
block = 20
screen = p.display.set_mode((X,Y))
p.display.set_caption("Snake")
back = p.image.load("/Users/mukhametaliissayev/Downloads/snake_fon.jpg")
back = p.transform.scale(back,(800,800))

#Creating a snake
snake_head = [100,50]
snake_body = [[100,50], [80, 50], [60, 50]]
snake_dir = "RIGHT"
change_to = snake_dir

#Creating an apple
food_pos = [random.randint(block, X-block), random.randint(block, Y-block)]
food = p.image.load("/Users/mukhametaliissayev/Downloads/apple.png")
food = p.transform.scale(food, (30,30))
food1 = p.transform.scale(food, (40,40))

#Setting up fonts
font = p.font.SysFont("Arial",40)
font_big = p.font.SysFont("Sand",70)
game_over = font_big.render("Game Over", True, (0,0,0))

#Setting up buttons
qquit = p.image.load("/Users/mukhametaliissayev/Downloads/quit.png")
qquit = p.transform.scale(qquit, (125,102))
restart = p.image.load("/Users/mukhametaliissayev/Downloads/restart.png")
restart = p.transform.scale(restart, (125,90))

#Other variables for programm
SPEED = 5
score = 0
level = 1
collision = False
run = True

#Main loop
while run:
    for i in p.event.get():
        if i.type == p.QUIT:
            run = False
            
        if i.type == p.KEYDOWN and not collision:
            if i.key == p.K_UP and snake_dir != "DOWN":
                change_to = "UP"
            if i.key == p.K_DOWN and snake_dir != "UP":
                change_to = "DOWN"
            if i.key == p.K_LEFT and snake_dir != "RIGHT":
                change_to = "LEFT"
            if i.key == p.K_RIGHT and snake_dir != "LEFT":
                change_to = "RIGHT"

        if i.type == p.MOUSEBUTTONDOWN and collision:
            mouse_pos = p.mouse.get_pos()
            restart_rect = restart.get_rect(topleft = (250,373))
            if restart_rect.collidepoint(mouse_pos):
                time.sleep(0.5)
                score = 0
                SPEED = 5
                level = 1
                snake_head = [100,50]
                snake_body = [[100,50], [80, 50], [60, 50]]
                snake_dir = "RIGHT"
                change_to = snake_dir
                collision = False
                hit_sound = False
            
            qquit_rect = qquit.get_rect(topleft = (450, 367))
            if qquit_rect.collidepoint(mouse_pos):
                time.sleep(0.5)
                run = False

    #Chenging snake
    snake_dir = change_to
    if snake_dir == "UP":
        snake_head[1] -= SPEED
    elif snake_dir == "DOWN":
        snake_head[1] += SPEED
    elif snake_dir == "LEFT":
        snake_head[0] -= SPEED
    elif snake_dir == "RIGHT":
        snake_head[0] += SPEED

    snake_body.insert(0, list(snake_head))


    #Checking for collisions
    if snake_head[0] <= 0 or snake_head[0] >= X or snake_head[1] <= 0 or snake_head[1] >= Y:
        collision = True

    for i in snake_body[1:]:
        if snake_head == i:
            collision = True


    #collecting apples
    if snake_head[0] >= food_pos[0] - 15 and snake_head[0] <= food_pos[0] + 25:
        if snake_head[1] >= food_pos[1] - 15 and snake_head[1] <= food_pos[1] + 25:
            score += 1
            food_pos = [random.randint(block, X-block), random.randint(block, Y-block)]
            snake_body.append(list(snake_body[-1]))
            if score % 4 == 0 and score != 0:
                SPEED += 1
                level += 1
            snake_body.pop()
    else:
        snake_body.pop()



    #display before and after
    if not collision:
        screen.blit(back,(0,0))
        for i in snake_body:
            p.draw.rect(screen, (255,255,255), p.Rect(i[0],i[1],block, block))
        screen.blit(food,food_pos)
        scores = font.render(str(score), True, (0,0,0))
        levels = font.render(f"Level:{level}", True, (0,0,0))
        screen.blit(levels,(350,20))
        screen.blit(food1, (X-88,23))
        screen.blit(scores,(X-40,20))
        if score >= 10:
            p.draw.rect(screen,(0,0,0),p.Rect(X-90,24,90,40),2)
        else:
            p.draw.rect(screen,(0,0,0),p.Rect(X-90,24,75,40),2)
    else:
        screen.blit(back, (0,0))
        screen.blit(game_over, (280,200))
        screen.blit(restart,(250,373))
        screen.blit(qquit,(450,367))
        screen.blit(food1, (X-88,23))
        screen.blit(scores,(X-40,20))
        if score >= 10:
            p.draw.rect(screen,(0,0,0),p.Rect(X-90,24,90,40),2)
        else:
            p.draw.rect(screen,(0,0,0),p.Rect(X-90,24,75,40),2)
        p.display.update()


    p.display.update()
    clock.tick(60)