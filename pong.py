#Library imports
import pygame
import random

#Initialize Pygame
pygame.init()

#Set up screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

#Define paddle and ball properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
AI_SPEED = 5

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

#Initialize paddles and ball
player_paddle = pygame.Rect(50, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect((SCREEN_WIDTH // 2) - (BALL_SIZE // 2), (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2), BALL_SIZE, BALL_SIZE)

#Ball speed
ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

#Score tracking
player_score = 0
aio_score = 0
winning_score = 6

#Font for displaying score
font = pygame.font.Font(None, 50)

#Main game loop
running = True
while running:
    screen.fill(BLACK)
    
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += PADDLE_SPEED
    
    #AI paddle movement
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += AI_SPEED
    if ai_paddle.centery > ball.centery:
        ai_paddle.y -= AI_SPEED
    
    #Ball movement
    ball.x += ball_dx
    ball.y += ball_dy
    
    #Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy *= -1
    
    #Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_dx *= -1
        ball_dx *= 1.1  # Slight speed increase after hitting a paddle
    
    #Scoring
    if ball.left <= 0:
        aio_score += 1
        ball.x = (SCREEN_WIDTH // 2) - (BALL_SIZE // 2)
        ball.y = (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2)
        ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
    
    if ball.right >= SCREEN_WIDTH:
        player_score += 1
        ball.x = (SCREEN_WIDTH // 2) - (BALL_SIZE // 2)
        ball.y = (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2)
        ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
    
    #Draw elements
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    #Display scores
    player_text = font.render(str(player_score), True, WHITE)
    ai_text = font.render(str(aio_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
    screen.blit(ai_text, (3 * SCREEN_WIDTH // 4, 20))
    
    #Check for win condition
    if player_score >= winning_score:
        win_text = font.render("Player Wins! Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    elif aio_score >= winning_score:
        win_text = font.render("AI Wins! Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    
    pygame.display.flip()
    pygame.time.delay(30)

#Restart or Quit
restart = True
while restart:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            restart = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_score = 0
                aio_score = 0
                ball.x = (SCREEN_WIDTH // 2) - (BALL_SIZE // 2)
                ball.y = (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2)
                ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
                ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
                running = True
                restart = False
            if event.key == pygame.K_q:
                restart = False

pygame.quit()
