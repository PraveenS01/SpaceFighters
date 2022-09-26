# importing pygame
import pygame

# importing random
import random

# importing math
import math

# importing mixer from pygame
from pygame import mixer

# initialising pygame
pygame.init()

# setting up icon and title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('1067357.png')
pygame.display.set_icon(icon)

# setting up player
player_ = pygame.image.load('2590218.png')
playerX = 368
playerY = 500
m = 0


def player(x, y):
    screen.blit(player_, (x, y))


# setting up the enemies
enemy_ = []
enemyX = []
enemyY = []
m1 = []
m2 = []
no_enemies = 6
for i in range(no_enemies):
    enemy_.append(pygame.image.load('2776831.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    m1.append(4)
    m2.append(40)


def enemy(x, y, k):
    screen.blit(enemy_[k], (x, y))


# setting up the background
bg = pygame.image.load('bg.png')

# bullet
bullet_state = 'ready'
bullet_ = pygame.image.load('222862.png')
bulletY = 500
bullet_change = 15
bulletX = playerX


def bullet(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bullet_, (x + 16, y + 10))


# collision
def isCollision(enemyX1, enemyY1, bulletX1, bulletY1):
    dis = math.sqrt((math.pow(enemyX1 - bulletX1, 2)) + (math.pow(enemyY1 - bulletY1, 2)))
    if dis < 27:
        return True
    else:
        return False


# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10


def score_display(s, x, y):
    score = font.render('Score :' + str(s), True, (255, 255, 255))
    screen.blit(score, (x, y))


# setting up the bgm
mixer.music.load('background.wav')
mixer.music.play(-1)

# game Over
font_over = pygame.font.Font('freesansbold.ttf', 64)


def gameOver():
    game_over = font_over.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                m = -5
            if event.key == pygame.K_RIGHT:
                m = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                m = 0
    playerX += m
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(no_enemies):
        if enemyY[i] > 430 and abs(enemyX[i] - playerX) < 32:
            for j in range(no_enemies):
                enemyY[j] = 1000
            gameOver()
            break
        enemyX[i] += m1[i]
        if enemyX[i] <= 0:
            m1[i] = 4
            enemyY[i] += m2[i]
        elif enemyX[i] >= 736:
            m1[i] = -4
            enemyY[i] += m2[i]
        col = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)
        score_display(score_value, scoreX, scoreY)
    if bullet_state == 'fired':
        bullet(bulletX, bulletY)
        bulletY -= bullet_change
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = 'ready'
    player(playerX, playerY)
    pygame.display.update()

pygame.quit()
# End Game