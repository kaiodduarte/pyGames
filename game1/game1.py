# GAME 1 :: exemplo basico
# tutorial de python: http://www.tutorialspoint.com/python/

import sys, pygame

pygame.init()

# tupla eh uma lista imutavel, parenteses eh opcional
# size = (width, height) = 640, 480
width = 640
height= 480
size = (width, height)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

ball_image = pygame.image.load("ball.png")
ball_rect = ball_image.get_rect()
ball_speed = [6, 6] # lista eh mutavel
ball_pos = [0, 0]

while True:
    for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()

    # move a bola
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # ricocheteia nos limites da tela
    if ball_pos[0] < 0 or ball_pos[0] > width - ball_rect.width:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] < 0 or ball_pos[1] > height- ball_rect.height:
        ball_speed[1] = -ball_speed[1]

    # preenche superficie (tela) com preto
    screen.fill(black)

    # desenha a bola
    ball_rect.x = ball_pos[0]
    ball_rect.y = ball_pos[1]
    screen.blit(ball_image, ball_rect)

    # troca back buffer (double buffer)
    pygame.display.flip()

    # limita jogo a 60 fps
    clock.tick(60)

