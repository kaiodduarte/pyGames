# GAME 1 :: exemplo basico
# tutorial de python: http://www.tutorialspoint.com/python/
 
import sys
import pygame
import random
 
## GLOBAIS #####################################################
 
# tupla eh uma lista imutavel, parenteses eh opcional
width = 1024
height= 600
size = (width, height)
black = (0, 0, 0)
BALLS_NUMBER = 10
balls = None
picked = 0
game_over = False
 
pygame.font.init()
font = pygame.font.Font(None, 30)
 
def update_text():
    global text
    text = font.render("SCORE: " + str(picked), 1, (255,255,255))
 
## CLASSES #####################################################
 
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
class GameObject:
    def __init__(self, screen, x, y, speed_x, speed_y, surface, offset):
        self.sprite = surface
        self.rect = self.sprite.get_rect()
        self.speed = Vector2(speed_x, speed_y)
        self.pos = Vector2(x, y)
        self.screen = screen
        self.visible = True
        self.offset = offset
        self.size = Vector2(self.rect.width, self.rect.height)
 
    def update_rect(self, offset):
        self.rect.x = self.pos.x + offset
        self.rect.y = self.pos.y + offset
        self.rect.width = self.size.x - offset*2
        self.rect.height= self.size.y - offset*2
 
    def render(self):
        if self.visible:
            # desenha a bola
            self.update_rect(0)
            screen.blit(self.sprite, self.rect)
 
    def collides_width(self, game_object):
        self.update_rect(self.offset)
        game_object.update_rect(game_object.offset)
        return self.rect.colliderect(game_object.rect)
 
 
class Ball(GameObject):
    def __init__(self, screen, x, y, speed_x, speed_y, surface, type):
        self.type = type
        GameObject.__init__(self, screen, x, y, speed_x, speed_y, surface, 18)
 
    def update(self):
        # pisca objeto
        #self.visible = not self.visible
 
        # move a bola
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y
 
        # ricocheteia nos limites da tela
        if self.pos.x < 0 or self.pos.x > width - self.rect.width:
            self.speed.x = -self.speed.x
        if self.pos.y < 0 or self.pos.y > height- self.rect.height:
            self.speed.y = -self.speed.y
 
class Background(GameObject):
    def __init__(self, screen, surface):
        GameObject.__init__(self, screen, 0, 0, 0, 0, surface, 0)
 
class Player(GameObject):
    def __init__(self, screen, x, y, speed, frames):
        self.max_speed = speed
        self.frames = frames
        GameObject.__init__(self, screen, x, y, 0, 0, frames[0], 18)
 
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.speed.x = -self.max_speed
            self.speed.y = 0
            self.sprite = self.frames[1]
        elif keys[pygame.K_RIGHT]:
            self.speed.x = self.max_speed
            self.speed.y = 0
            self.sprite = self.frames[0]
        elif keys[pygame.K_UP]:
            self.speed.x = 0
            self.speed.y = -self.max_speed
            self.sprite = self.frames[2]
        elif keys[pygame.K_DOWN]:
            self.speed.x = 0
            self.speed.y = self.max_speed
            self.sprite = self.frames[3]
 
        # move jogador
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y
 
        # wrap screen
        if self.pos.x < -self.rect.width/2:
            self.pos.x = width - self.rect.width/2
        elif self.pos.x > width - self.rect.width/2:
            self.pos.x = -self.rect.width/2
 
        if self.pos.y < -self.rect.height/2:
            self.pos.y = height - self.rect.height/2
        elif self.pos.y > height - self.rect.height/2:
            self.pos.y = -self.rect.height/2
 
 
## JOGO ########################################################
 
def gameInit():
    pygame.init()
    global screen, clock
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
 
    global ball_sprite_red
    ball_sprite_red = pygame.image.load("circle_red.png")
    global ball_sprite_green
    ball_sprite_green = pygame.image.load("circle_green.png")
 
    global player
    player_right = pygame.image.load("player.png")
    player_left  = pygame.transform.rotate(player_right, 180)
    player_up    = pygame.transform.rotate(player_right, 90)
    player_down  = pygame.transform.rotate(player_right,-90)
    x = width / 2 - player_right.get_rect().width / 2
    frames = (player_right, player_left, player_up, player_down)
    player = Player(screen, x, height - 200, 5, frames)
 
    global balls
    balls = []
 
    global ball_spawner
    spawner_img = pygame.image.load("square.png")
    spawner_img = pygame.transform.rotate(spawner_img, 45)
    x = width/2 - spawner_img.get_rect().width/2
    y = height/2 - spawner_img.get_rect().height/2
    ball_spawner = Ball(screen, x, y, 0, 0, spawner_img, None)
 
    global background
    background = Background(screen, pygame.image.load("background.png"))
 
    global game_over_img
    game_over_img = pygame.image.load("texto_fim_de_jogo.png")
 
    global ball_delay
    ball_delay = 60
    global ball_count
    ball_count = 0
 
    global picked
    picked = 0
    update_text()
    global game_over
    game_over = False
 
def gameInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
 
    global keys
    keys = pygame.key.get_pressed()
 
    if keys[pygame.K_ESCAPE]: sys.exit()
 
 
def spawn_ball():
    global ball_count
    ball_count += 1
    if ball_count >= ball_delay:
        ball_count = 0
        # lanca bola no meio da tela
        x = width/2 - ball_sprite_red.get_rect().width/2
        y = height/2 - ball_sprite_red.get_rect().height/2
        speed_x = random.uniform(0, 10) - 5
        speed_y = random.uniform(0, 10) - 5
 
        if random.randint(0, 1) == 0:
            img = ball_sprite_red
            type = "red"
        else:
            img = ball_sprite_green
            type = "green"
 
        balls.append(Ball(screen, x, y, speed_x, speed_y, img, type))
 
def gameUpdate():
    if game_over and keys[pygame.K_SPACE]:
        gameInit()
 
    if not game_over:
        spawn_ball()
        player.update(keys)
 
    for ball in balls:
        ball.update()
 
    if not game_over:
        for ball in balls:
            if ball.collides_width(player):
                if ball.type == "green":
                    balls.remove(ball)
                    global picked
                    picked += 10
                    update_text()
                else:
                    global game_over
                    game_over = True
 
def gameRender():
    # preenche superficie (tela) com preto
    screen.fill(black)
 
    background.render()
 
    for ball in balls:
        ball.render()
 
    ball_spawner.render()
 
    if game_over:
        game_over_rect = game_over_img.get_rect()
        game_over_rect.x = 50
        game_over_rect.y = 200
        screen.blit(game_over_img, game_over_rect)
    else:
        player.render()
 
 
    screen.blit(text, text.get_rect())
 
    # troca back buffer (double buffer)
    pygame.display.flip()
 
 
## MAIN ########################################################
 
gameInit()
 
while True:
    gameInput()
    gameUpdate()
    gameRender()
 
    # limita jogo ao fps
    clock.tick(30)