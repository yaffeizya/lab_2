import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
x, y = 400,300
run = True
clock = pygame.time.Clock()
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and y >= 25: y -= 20
    if pressed[pygame.K_DOWN]and y <= 575: y += 20
    if pressed[pygame.K_LEFT] and x >= 25: x -= 20
    if pressed[pygame.K_RIGHT] and x <= 775: x += 20

    screen.fill((255,255,255))
    pygame.draw.circle(screen, (200,0,0), (x,y), 25)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()