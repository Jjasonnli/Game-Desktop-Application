import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 5

# Set up the ball
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 3 * random.choice([-1, 1])
ball_dy = -3
ball = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Set up the bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
num_bricks = 10
bricks = []
for i in range(num_bricks):
    brick_color = random.choice([BLUE, RED, GREEN])
    brick_x = i * (BRICK_WIDTH + 5) + 30
    brick_y = 50
    bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Move the ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Handle ball collisions with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx *= -1
    if ball.top <= 0:
        ball_dy *= -1

    # Handle ball collisions with the paddle
    if ball.colliderect(pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)):
        ball_dy *= -1

    # Handle ball collisions with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy *= -1
            break

    # Check if the ball hit the bottom wall (game over condition)
    if ball.bottom >= HEIGHT:
        game_over = True

    # Clear the screen
    win.fill(WHITE)

    # Draw the paddle, ball, and bricks
    pygame.draw.rect(win, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(win, RED, (ball.x, ball.y), BALL_RADIUS)
    for brick in bricks:
        brick_color = random.choice([BLUE, RED, GREEN])
        pygame.draw.rect(win, brick_color, brick)

    pygame.display.update()
    clock.tick(60)

# Game over, quit Pygame
pygame.quit()