#Imports
import pygame as p
import random, time

#Initialzing 
p.init()

#Setting up background music
p.mixer.music.load("/Users/mukhametaliissayev/Downloads/back_music.wav")
p.mixer.music.play(-1)

#Creating Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Setting up FPS
FPS = 60
timee = p.time.Clock()

#Variables to use in Programm
SCORE_CARS = 0
SCORE_COINS = 0
SPEED = 5

#Setting up Fonts
font = p.font.SysFont("Verdana", 40)
font_big = p.font.SysFont("Verdana", 60)
game_over = font_big.render("Game Over", True, BLACK)

#Create a screen
X = 600
Y = 800
screen = p.display.set_mode((X,Y))
screen.fill(WHITE)
p.display.set_caption("Racer")

back = p.image.load("/Users/mukhametaliissayev/Downloads/fon.png")
back = p.transform.scale(back, (X,Y))

#Import images of buttons
restart = p.image.load("/Users/mukhametaliissayev/Downloads/restart.png")
qquit = p.image.load("/Users/mukhametaliissayev/Downloads/quit.png")
restart = p.transform.scale(restart, (125,100))
qquit = p.transform.scale(qquit, (130,110))

#Creating class of Enemy
class Enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.image.load("/Users/mukhametaliissayev/Downloads/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(80,X-80),0)

    def move(self):
        global SCORE_CARS
        self.rect.move_ip(0,SPEED)
        if self.rect.top > Y:
            SCORE_CARS += 1
            self.rect.top = 0
            self.rect.center = (random.randint(80,X-80),0)

#Creating class of main character
class Player(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.image.load("/Users/mukhametaliissayev/Downloads/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (X-100, Y-100)

    def move(self):
        pressed = p.key.get_pressed()
        if self.rect.left > 0:
            if pressed[p.K_LEFT]: self.rect.move_ip(-5, 0)
        if self.rect.right < X:
            if pressed[p.K_RIGHT]: self.rect.move_ip(5, 0)

#Creating class of coins
class Coin(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.image.load("/Users/mukhametaliissayev/Downloads/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(80, X-80),0)
        self.cnt = 0

    def move(self):
        if self.cnt > 0:
            self.cnt -= 1
            return
        self.rect.move_ip(0,SPEED)
        if self.rect.top > Y:
            self.rect.top = 0
            self.rect.center = (random.randint(80, X-80),-20)
            self.cnt = 60
            

#Setting up Splrites
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating sprites group
enemies = p.sprite.Group()
enemies.add(E1)
coins = p.sprite.Group()
coins.add(C1)
all_spites = p.sprite.Group()
all_spites.add(P1)
all_spites.add(C1)
all_spites.add(E1)

#Adding new user event
plus_speed = p.USEREVENT + 1
p.time.set_timer(plus_speed, 1000)

#image for top right corner
image_of_coin = p.image.load("/Users/mukhametaliissayev/Downloads/coin.png")
image_of_coin = p.transform.scale(image_of_coin, (40,40))

#Initial game states
game_over_state = False
run = True

#Main game loop
while run:
    for i in p.event.get():
        if i.type == p.QUIT:
            run = False
        if i.type == plus_speed and not game_over_state:
            SPEED += 0.5

        #Checking if mouse is clicked
        if i.type == p.MOUSEBUTTONDOWN and game_over_state:
            mouse_pos = p.mouse.get_pos()
            p.mixer.Sound("/Users/mukhametaliissayev/Downloads/mouse_click.mp3").play()
            restart_rect = restart.get_rect(topleft = (140, 373))
            if restart_rect.collidepoint(mouse_pos):
                SCORE_CARS = 0
                SCORE_COINS = 0
                SPEED = 5
                P1 = Player()
                E1 = Enemy()
                C1 = Coin()
                enemies = p.sprite.Group()
                enemies.add(E1)
                coins = p.sprite.Group()
                coins.add(C1)
                all_spites = p.sprite.Group()
                all_spites.add(P1)
                all_spites.add(C1)
                all_spites.add(E1)
                game_over_state = False
                p.mixer.music.play(-1)
            quit_rect = qquit.get_rect(topleft = (340, 367))
            if quit_rect.collidepoint(mouse_pos):
                run = False

    if not game_over_state:
        screen.blit(back, (0,0))
        scores = font.render(str(SCORE_CARS), True, BLACK)
        scores1 = font.render(str(f":{SCORE_COINS}"), True, BLACK)
        screen.blit(scores, (10,10))
        screen.blit(scores1, (X-60, 10))
        screen.blit(image_of_coin, (X-95,18))


        for i in all_spites:
            screen.blit(i.image, i.rect)
            i.move()
    else:
        p.mixer.music.stop()
        screen.blit(back, (0,0))
        screen.blit(game_over, (130,200))
        screen.blit(restart, (140,373))
        screen.blit(qquit, (340,367))

    #Checking collision with enemies
    if p.sprite.spritecollideany(P1, enemies) and not game_over_state:
        p.mixer.Sound(" /Users/mukhametaliissayev/Downloads/crash.wav").play()
        time.sleep(0.5)
        game_over_state = True
        for i in all_spites:
            i.kill()
        
    #Checking collision with coins 
    if p.sprite.spritecollideany(P1, coins) and not game_over_state:
        SCORE_COINS += 1
        p.mixer.Sound("/Users/mukhametaliissayev/Downloads/collect.mp3").play()
        C1.cnt = 60
        C1.rect.top = 0
        C1.rect.center = (random.randint(80, X-80),-20)
        p.display.update()


    p.display.update()
    timee.tick(FPS)