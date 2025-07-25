import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Snake Game (Termux)")

# Snake and food
snake_block = 10
snake_speed = 15

# Fonts
font = pygame.font.SysFont(None, 30)

def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [WIDTH / 6, HEIGHT / 3])

def generate_food(snake_list):
    while True:
        food_x = round(random.randrange(snake_block, WIDTH - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(snake_block, HEIGHT - snake_block) / snake_block) * snake_block
        food_position = [food_x, food_y]
        if food_position not in snake_list:
            return food_position

def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH / 2, HEIGHT / 2
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1

    food_pos = generate_food(snake_list)
    food_x, food_y = food_pos

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        x += x_change
        y += y_change

        # Boundary check
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, GREEN, [food_x, food_y, snake_block, snake_block])

        # Update snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake hits itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake
        for segment in snake_list:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], snake_block, snake_block])

        # Score display
        score_text = font.render(f"Score: {snake_length - 1}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_pos = generate_food(snake_list)
            food_x, food_y = food_pos
            snake_length += 1

        if game_close:
            while game_close:
                screen.fill(BLACK)
                message("Game Over! Press Q-Quit or C-Play Again", RED)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop()

        clock.tick(snake_speed)

    pygame.quit()

# Start the game
game_loop()
