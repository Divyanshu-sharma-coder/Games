import pygame
import random
import sys
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Escape")
clock = pygame.time.Clock()

# Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.score = 0

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and not maze[new_y][new_x]:
            self.x, self.y = new_x, new_y

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Enemy (chases player)
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5

    def move_towards(self, player, maze):
        # Simple BFS pathfinding
        q = deque()
        q.append((self.x, self.y, []))
        visited = set()
        visited.add((self.x, self.y))

        while q:
            x, y, path = q.popleft()
            if (x, y) == (player.x, player.y):
                if path and len(path) > 1:
                    self.x, self.y = path[1]  # Move along path
                break
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and not maze[ny][nx] and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny, path + [(nx, ny)]))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Treasure
class Treasure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self):
        if not self.collected:
            pygame.draw.rect(screen, GOLD, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

# Maze generation (Depth-First Search)
def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        moved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < COLS - 1 and 0 < ny < ROWS - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0  # Remove wall
                stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()

    return maze

# Game setup
def setup_game():
    maze = generate_maze()
    player = Player(1, 1)
    enemies = [Enemy(COLS - 2, ROWS - 2)]
    treasures = [Treasure(random.randint(1, COLS - 2), random.randint(1, ROWS - 2)) for _ in range(3)]
    return maze, player, enemies, treasures

# Main game loop
def main():
    maze, player, enemies, treasures = setup_game()
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move(-1, 0, maze)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move(1, 0, maze)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move(0, -1, maze)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move(0, 1, maze)

        # Enemy movement
        for enemy in enemies:
            enemy.move_towards(player, maze)

        # Treasure collection
        for treasure in treasures:
            if not treasure.collected and player.x == treasure.x and player.y == treasure.y:
                treasure.collected = True
                player.score += 10
                treasures.append(Treasure(random.randint(1, COLS - 2), random.randint(1, ROWS - 2)))

        # Collision with enemies
        for enemy in enemies:
            if player.x == enemy.x and player.y == enemy.y:
                print("Game Over! Score:", player.score)
                maze, player, enemies, treasures = setup_game()

        # Draw everything
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for treasure in treasures:
            treasure.draw()

        for enemy in enemies:
            enemy.draw()

        player.draw()

        # Display score
        score_text = font.render(f"Score: {player.score}", True, GREEN)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
