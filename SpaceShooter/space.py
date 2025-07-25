import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Termux Space Shooter")
clock = pygame.time.Clock()

# Game objects
player_pos = [WIDTH // 2, HEIGHT - 50]
player_speed = 5
bullets = []
enemies = []
bullet_cooldown = 0
score = 0
font = pygame.font.Font(None, 36)

def draw_spaceship(x, y):
    pygame.draw.polygon(screen, GREEN, [
        (x, y - 20),
        (x - 15, y + 15),
        (x + 15, y + 15)
    ])

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x - 15, y - 10, 30, 20))

def spawn_enemy():
    x = random.randint(30, WIDTH - 30)
    y = random.randint(-100, -40)
    enemies.append([x, y, 2])

def main():
    global bullet_cooldown, score, player_pos

    for _ in range(5):
        spawn_enemy()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 30:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 30:
            player_pos[0] += player_speed

        bullet_cooldown += 1
        if bullet_cooldown >= 15:
            bullets.append([player_pos[0], player_pos[1] - 20])
            bullet_cooldown = 0

        for bullet in bullets[:]:
            bullet[1] -= 10
            if bullet[1] < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy[1] += enemy[2]
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                spawn_enemy()

            for bullet in bullets[:]:
                if abs(bullet[0] - enemy[0]) < 20 and abs(bullet[1] - enemy[1]) < 20:
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 10
                    spawn_enemy()
                    break

            if abs(player_pos[0] - enemy[0]) < 30 and abs(player_pos[1] - enemy[1]) < 30:
                running = False

        screen.fill(BLACK)
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (bullet[0], bullet[1]), 3)
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        draw_spaceship(player_pos[0], player_pos[1])
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
