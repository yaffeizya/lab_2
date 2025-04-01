#Imports
import pygame as p
import time

#Initialzing 
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
drawing_square = False
drawing_r_trng = False
drawing_e_trng = False
drawing_rhomb = False
cur_tool = 0
points = []
timer = time.time()

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
    ("Brush", p.Rect(240, 10, 60, 30), 0),
    ("Rect", p.Rect(310, 10, 60, 30), 1),
    ("Circle", p.Rect(380, 10, 60, 30), 2),
    ("Eraser", p.Rect(450, 10, 60, 30), 3),
    ("Square", p.Rect(520, 10, 60, 30), 4),
    ("R_Trng", p.Rect(590, 10, 60, 30), 5),
    ("E_Trng", p.Rect(660, 10, 60, 30), 6),
    ("Rhomb", p.Rect(730, 10, 60, 30), 7)
]

def drawLineBetween(screen, start, end, width, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy), 1)
    for i in range(distance + 1):
        t = i / distance
        x = int(start[0] + t * dx)
        y = int(start[1] + t * dy)
        p.draw.circle(screen, color, (x, y), width)
    
def drawrectBetween(screen, start, end, width, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy), 1)
    for i in range(distance + 1):
        t = i / distance
        x = int(start[0] + t * dx)
        y = int(start[1] + t * dy)
        p.draw.rect(screen, color, (x, y))

#Main loop
run = True
while run:
    for i in p.event.get():
        if i.type == p.QUIT:
            run = False
        if i.type == p.MOUSEBUTTONDOWN:
            #increasin the size of brush
            if i.button == 4:
                brush_size += 1
            if i.button == 5 and brush_size > 1:
                brush_size -= 1

            #checking if button of the color clicked
            pos = p.mouse.get_pos()
            for color, rect in colors_button:
                if rect.collidepoint(pos):
                   cur_color = color
                   tool = 0
                   break

            #checking if the button of tools clicked
            for _, rcet, tool in tools_button:
                if rcet.collidepoint(pos):
                    cur_tool = tool
                    break
            start_pos = pos
            if cur_tool == 0: 
                drawing = True
                points = [pos]
            else: drawing = False
            if cur_tool == 1: drawing_rect = True
            else: drawing_rect = False
            if cur_tool == 2: drawing_circle = True
            else: drawing_circle = False
            if cur_tool == 3: 
                erasing = True
                points = [pos]
            else: erasing = False
            if cur_tool == 4: drawing_square = True
            else: drawing_square = False
            if cur_tool == 5: drawing_r_trng = True
            else: drawing_r_trng = False
            if cur_tool == 6: drawing_e_trng = True
            else: drawing_e_trng = False
            if cur_tool == 7: drawing_rhomb = True
            else: drawing_rhomb = False


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

            elif drawing_square:
                end_pos = p.mouse.get_pos()
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                right = min(width, height)
                p.draw.rect(screen, cur_color, (x, y, right, right))

            elif drawing_r_trng:
                end_pos = p.mouse.get_pos()
                first_point = start_pos
                third_point = end_pos
                second_point = [0, 0]
                if (first_point[0] > third_point[0] and first_point[1] < third_point[1]) or (first_point[0] < third_point[0] and first_point[1] > third_point[1]):
                    second_point[0] = max(first_point[0], third_point[0])
                    second_point[1] = max(first_point[1], third_point[1])
                else:
                    second_point[0] = min(first_point[0], third_point[0])
                    second_point[1] = max(first_point[1], third_point[1])
                p.draw.polygon(screen, cur_color, (first_point, second_point, third_point))

            elif drawing_e_trng:
                end_pos = p.mouse.get_pos()
                top_corner_x = min(start_pos[0], end_pos[0])
                top_corner_y = min(start_pos[1], end_pos[1])
                lower_corner_x  = max(start_pos[0], end_pos[0])
                lower_corner_y = max(start_pos[1], end_pos[1])
                first_point = [lower_corner_x, lower_corner_y]
                second_point = [(top_corner_x + lower_corner_x) / 2, top_corner_y]
                third_point = [top_corner_x, lower_corner_y]
                p.draw.polygon(screen, cur_color, (first_point, second_point, third_point))

            elif drawing_rhomb:
                end_pos = p.mouse.get_pos()
                top_corner_x = min(start_pos[0], end_pos[0])
                top_corner_y = min(start_pos[1], end_pos[1])
                lower_corner_x  = max(start_pos[0], end_pos[0])
                lower_corner_y = max(start_pos[1], end_pos[1])
                first_point = [(top_corner_x + lower_corner_x) / 2, top_corner_y]
                second_point = [lower_corner_x, (top_corner_y + lower_corner_y) / 2]
                third_point = [top_corner_x, (top_corner_y + lower_corner_y) / 2]
                fourth_point = [(top_corner_x + lower_corner_x) / 2, lower_corner_y]
                p.draw.polygon(screen, cur_color, (first_point, third_point, fourth_point, second_point))

            drawing = False
            drawing_rect = False
            drawing_circle = False
            erasing = False
            drawing_square = False
            drawing_r_trng = False
            drawing_e_trng = False
            drawing_rhomb = False
            points = []

        #do things if the mouse is moving
        if i.type == p.MOUSEMOTION:
            if drawing:
                pos = p.mouse.get_pos()
                points.append(pos)
                if len(points) > 1:
                    drawLineBetween(screen, points[-2], points[-1], brush_size, cur_color)
            elif erasing:
                pos = p.mouse.get_pos()
                points.append(pos)
                if len(points) > 1:
                    drawLineBetween(screen, points[-2], points[-1], brush_size, WHITE)
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
            elif drawing_square:
                end_pos = p.mouse.get_pos()
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                right = min(width, height)
                p.draw.rect(screen, cur_color, (x, y, right, right),100)

    #increasing size of the brush & delete all from window
    pressed = p.key.get_pressed()
    if pressed[p.K_UP]: brush_size += 1
    if pressed[p.K_DOWN] and brush_size > 1: brush_size -= 1
    if pressed[p.K_c]: screen.fill((255,255,255))

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

                