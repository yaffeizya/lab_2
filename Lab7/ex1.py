import pygame
import datetime 
pygame.init()
screen=pygame.display.set_mode((800, 600))
run=True
clock=pygame.time.Clock()
back=pygame.image.load('/Users/mukhametaliissayev/Desktop/clock.png')
r_hand=pygame.image.load('/Users/mukhametaliissayev/Desktop/min_hand.png')
l_hand=pygame.image.load('/Users/mukhametaliissayev/Desktop/sec_hand.png')
now=datetime.datetime.now()
sec=now.second; seconds= -sec*6
minn = now.minute;minutes = -minn * 6
print(sec)
print(minn)
image_center = (400,300)




while run:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            run=False

    right_hand = pygame.transform.rotate(r_hand,minutes)
    minutes -= 1/600
    right = right_hand.get_rect(center = image_center)

    left_hand = pygame.transform.rotate(l_hand,seconds)
    seconds -= 1/10
    left = left_hand.get_rect(center = image_center)

    screen.blit(back, (0,0))
    screen.blit(right_hand, right)
    screen.blit(left_hand, left)

    pygame.display.flip()   
    clock.tick(60) 