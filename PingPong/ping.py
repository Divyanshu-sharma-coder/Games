import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Termux Pong - Touch Controls")
clock = pygame.time.Clock()

# Game objects
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
ai_speed = 7
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return random.choice((6, -6)), random.choice((6, -6))

def ai_movement():
    # Slightly imperfect AI for fairness
    target_y = ball.centery + random.randint(-10, 10)
    if ai_paddle.centery < target_y:
        ai_paddle.y += ai_speed
    elif ai_paddle.centery > target_y:
        ai_paddle.y -= ai_speed
    ai_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, ai_paddle.y))

def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, ai_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision (top/bottom)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision (paddles)
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x *= -1.1  # Increase speed on hit

    # Scoring
    if ball.left <= 0:
        ai_score += 1
        ball_speed_x, ball_speed_y = reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        ball_speed_x, ball_speed_y = reset_ball()

def main():
    global player_speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Touch controls: Move paddle to touch position
                if event.type == pygame.FINGERDOWN:
                    touch_y = event.y * HEIGHT
                else:
                    touch_y = event.pos[1]
                player_paddle.centery = touch_y

        # Ensure paddle stays on screen
        player_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player_paddle.y))

        # AI movement
        ai_movement()

        # Ball movement
        ball_movement()

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, ai_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Score display
        player_text = font.render(f"Player: {player_score}", True, WHITE)
        ai_text = font.render(f"AI: {ai_score}", True, WHITE)
        screen.blit(player_text, (20, 20))
        screen.blit(ai_text, (WIDTH - 120, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
