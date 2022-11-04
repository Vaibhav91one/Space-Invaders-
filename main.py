import math
import random
import pygame
from pygame import mixer

# Pygame initialize
pygame.init()

# background Sound
mixer.music.load("Lil Uzi and Playboi Carti but they are extra chill - Lofi Mix - CHILLAF (320 kbps).mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

over_font = pygame.font.Font("Want Coffee.ttf", 64)

# Keeping Score
score = 0
score_X = 10
score_Y = 5
font = pygame.font.Font("Want Coffee.ttf", 32)

# Window Adjustment
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("science-fiction.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Background.png")

# Enemy
Enemy_img = []
enemy_X = []
enemy_Y = []
# Moving of the enemy
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    Enemy_img.append(pygame.image.load("alien.png"))
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    # Moving of the enemy
    enemy_x_change.append(5)
    enemy_y_change.append(40)


# Adding enemy to the window
def Enemy(x, y, n):
    screen.blit(Enemy_img[n], (x, y))


# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 460
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y))


# Player
Player_img = pygame.image.load("ufo.png")
player_X = 350
player_Y = 500

# Moving of the spaceship
player_x_change = 0


# Adding spaceship to the window
def Player(x, y):
    screen.blit(Player_img, (x, y))


def score_Display(x, y):
    score_val = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_val, (x, y))


def Game_over_Display():
    game_over_val = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_val, (250, 250))


def collision_detection(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))
    if distance <= 27:
        return True
    else:
        return False


running = True

# Main game loop
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if Cross is pressed to close the window
            running = False

        # Moving the spaceship left and right
        if event.type == pygame.KEYDOWN:
            # print("A key is pressed down")
            if event.key == pygame.K_LEFT:
                # print("Left key Pressed")
                player_x_change = -2

            if event.key == pygame.K_RIGHT:
                # print("Right key Pressed")
                player_x_change = 2

            # print("Space key Pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet_music = mixer.Sound("")
                    # bullet_music.play()
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            # print("A key is released")
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Adding player movement changes to the spaceship
    player_X += player_x_change

    if bullet_Y <= 0:
        bullet_Y = 460
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_y_change

    # cases if the spaceship hits boundaries
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    for i in range(number_of_enemies):
        # Game Over
        if enemy_Y[i] >= 460:
            for j in range(number_of_enemies):
                enemy_Y[j] = 2000
            Game_over_Display()
            break

        # enemy iterates through the x-axis by change of .3
        enemy_X[i] += enemy_x_change[i]

        # case if enemy hits boundaries
        if enemy_X[i] <= 0:
            enemy_x_change[i] = 4
            enemy_Y[i] += enemy_y_change[i]
        elif enemy_X[i] >= 736:
            enemy_x_change[i] = -4
            enemy_Y[i] += enemy_y_change[i]

        collision = collision_detection(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)

        if collision:
            # enemy_music = mixer.Sound("")
            # enemy_music.play()
            bullet_Y = 460
            bullet_state = "ready"
            score += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 150)
        Enemy(enemy_X[i], enemy_Y[i], i)

    Player(player_X, player_Y)
    score_Display(score_X, score_Y)
    pygame.display.update()
