import pygame as p

p.init()

#Setting up FPS
clock = p.time.Clock()

#Creating colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (122, 127, 128)

#Creating a screen
X = Y = 800
screen = p.display.set_mode((X, Y))
p.display.set_caption("Paint")
screen.fill(WHITE)

#Other variables for programm
cur_color = BLACK
brush_size = 5
drawing = False
drawing_rect = False
drawing_circle = False
erasing = False
cur_tool = 0

#Creating font
font = p.font.SysFont("Sand", 20)

#Setting up color buttons
colors_button = [
    (RED, p.Rect(10,10,30,30)),
    (GREEN, p.Rect(50,10,30,30)),
    (BLUE, p.Rect(90,10,30,30)),
    (YELLOW, p.Rect(130,10,30,30)),
    (BLACK, p.Rect(170,10,30,30)),
]

#Setting up tool buttons
tools_button = [
    ("Brush", p.Rect(300, 10, 60, 30), 0),
    ("Rect", p.Rect(370, 10, 60, 30), 1),
    ("Circle", p.Rect(440, 10, 60, 30), 2),
    ("Eraser", p.Rect(510, 10, 60, 30), 3)
]

#Main loop
run = True
while run:
    for i in p.event.get():
        if i.type == p.QUIT:
            run = False
        if i.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            for color, rect in colors_button:
                if rect.collidepoint(pos):
                   cur_color = color
                   tool = 0
                   break
            for _, rcet, tool in tools_button:
                if rcet.collidepoint(pos):
                    cur_tool = tool
                    break
            start_pos = pos
            if cur_tool == 0: drawing = True
            else: drawing = False
            if cur_tool == 1: drawing_rect = True
            else: drawing_rect = False
            if cur_tool == 2: drawing_circle = True
            else: drawing_circle = False
            if cur_tool == 3: erasing = True
            else: erasing = False


        if i.type == p.MOUSEBUTTONUP:
            if drawing_rect:
                end_pos = p.mouse.get_pos()
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                p.draw.rect(screen, cur_color, (x, y, width, height))
            elif drawing_circle:
                end_pos = p.mouse.get_pos()
                R = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                p.draw.circle(screen, cur_color, start_pos, R)
            drawing = False
            drawing_rect = False
            drawing_circle = False
            erasing = False


        if i.type == p.MOUSEMOTION:
            if drawing:
                pos = p.mouse.get_pos()
                p.draw.circle(screen, cur_color, pos, brush_size)
            elif erasing:
                pos = p.mouse.get_pos()
                p.draw.circle(screen, WHITE, pos, brush_size)
            elif drawing_rect:
                end_pos = p.mouse.get_pos()
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                p.draw.rect(screen, cur_color, (x, y, width, height),100)
            elif drawing_circle:
                end_pos = p.mouse.get_pos()
                R = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                p.draw.circle(screen, cur_color, start_pos, R, 100)

    pressed = p.key.get_pressed()
    if pressed[p.K_UP]: brush_size += 1
    if pressed[p.K_DOWN] and brush_size > 1: brush_size -= 1

    #drowing color buttons
    for color, rect in colors_button:
        p.draw.rect(screen, color, rect)
        p.draw.rect(screen, BLACK, rect, 1)

    #drawing tool buttons
    for name, rect, tool in tools_button:
        if cur_tool == tool:
            p.draw.rect(screen, GRAY, rect)
        else:
            p.draw.rect(screen, WHITE, rect)
        p.draw.rect(screen, BLACK, rect, 1)
        namee = font.render(name, True, BLACK)
        screen.blit(namee, (rect.x + 5, rect.y + 5))

    p.display.update()
    clock.tick(60)

                