import pygame
import os

pygame.init()

screen = pygame.display.set_mode((375, 812))
iphone = pygame.image.load('/Users/mukhametaliissayev/Downloads/phone.jpeg')
iphone = pygame.transform.scale(iphone, (375, 812))
music_dir = '/Users/mukhametaliissayev/Desktop/pygame/venv/mp3'
music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

if music_files:
    current_track = 0  
    pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))
    pygame.mixer.music.play()

font = pygame.font.SysFont(None, 30)
run = True
paused = False 

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break 

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True

            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(music_files)
                pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))
                pygame.mixer.music.play()

            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(music_files)
                pygame.mixer.music.load(os.path.join(music_dir, music_files[current_track]))
                pygame.mixer.music.play()

    
    screen.fill((255, 255, 255))
    screen.blit(iphone, (0, 0))

    if music_files:
        music_name = music_files[current_track].split('.')[0]
        text = font.render(music_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(375 // 2, 510))
        screen.blit(text, text_rect)

    pygame.display.flip()