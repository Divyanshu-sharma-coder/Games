import pygame
import random

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I - Cyan
    (0, 0, 255),    # J - Blue
    (255, 165, 0),  # L - Orange
    (255, 255, 0),  # O - Yellow
    (0, 255, 0),    # S - Green
    (128, 0, 128),  # T - Purple
    (255, 0, 0)     # Z - Red
]

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = CELL_SIZE

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    
    [[1, 0, 0],
     [1, 1, 1]],     # J
     
    [[0, 0, 1],
     [1, 1, 1]],     # L
     
    [[1, 1],
     [1, 1]],        # O
     
    [[0, 1, 1],
     [1, 1, 0]],     # S
     
    [[0, 1, 0],
     [1, 1, 1]],     # T
     
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

class Tetrimino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def rotate(self):
        # Transpose the shape matrix and reverse each row to rotate 90 degrees
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]

        return rotated

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, 
                            (GAME_AREA_LEFT + x * CELL_SIZE, y * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE), 1)
            if grid[y][x] > 0:
                pygame.draw.rect(screen, COLORS[grid[y][x] - 1], 
                                (GAME_AREA_LEFT + x * CELL_SIZE + 1, y * CELL_SIZE + 1, 
                                 CELL_SIZE - 2, CELL_SIZE - 2))

def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, 
                                (GAME_AREA_LEFT + (tetrimino.x + x) * CELL_SIZE + 1, 
                                 (tetrimino.y + y) * CELL_SIZE + 1, 
                                 CELL_SIZE - 2, CELL_SIZE - 2))

def valid_space(tetrimino, grid):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetrimino.y + y >= GRID_HEIGHT or 
                    tetrimino.x + x < 0 or 
                    tetrimino.x + x >= GRID_WIDTH or 
                    grid[tetrimino.y + y][tetrimino.x + x]):
                    return False
    return True

def check_lost(grid):
    return any(cell for cell in grid[0])

def clear_rows(grid, score):
    cleared_rows = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            cleared_rows += 1
            for y2 in range(y, 0, -1):
                grid[y2] = grid[y2-1].copy()
            grid[0] = [0 for _ in range(GRID_WIDTH)]
    
    # Update score based on cleared rows
    if cleared_rows == 1:
        score += 100
    elif cleared_rows == 2:
        score += 300
    elif cleared_rows == 3:
        score += 500
    elif cleared_rows == 4:
        score += 800
        
    return score

def draw_next_shape(tetrimino):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, WHITE)
    
    sx = GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20
    sy = 100
    
    screen.blit(label, (sx, sy - 40))
    
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, 
                                (sx + x * CELL_SIZE + 1, 
                                 sy + y * CELL_SIZE + 1, 
                                 CELL_SIZE - 2, CELL_SIZE - 2))

def draw_score(score):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    
    sx = GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20
    sy = 20
    
    screen.blit(label, (sx, sy))

def main():
    grid = create_grid()
    current_tetrimino = Tetrimino()
    next_tetrimino = Tetrimino()
    change_tetrimino = False
    run = True
    score = 0
    fall_time = 0
    fall_speed = 0.5  # seconds
    level_time = 0
    
    while run:
        # Increase fall speed as time passes
        level_time += clock.get_rawtime()
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.1:
                fall_speed -= 0.005
        
        fall_time += clock.get_rawtime()
        clock.tick()
        
        # Automatic falling
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_tetrimino.y += 1
            if not valid_space(current_tetrimino, grid) and current_tetrimino.y > 0:
                current_tetrimino.y -= 1
                change_tetrimino = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.x -= 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x += 1
                
                if event.key == pygame.K_RIGHT:
                    current_tetrimino.x += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x -= 1
                
                if event.key == pygame.K_DOWN:
                    current_tetrimino.y += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.y -= 1
                
                if event.key == pygame.K_UP:
                    rotated = current_tetrimino.rotate()
                    old_shape = current_tetrimino.shape
                    current_tetrimino.shape = rotated
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.shape = old_shape
        
        # Add tetrimino to the grid when it lands
        if change_tetrimino:
            for y, row in enumerate(current_tetrimino.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_tetrimino.y + y][current_tetrimino.x + x] = current_tetrimino.shape_idx + 1
            
            # Change to next tetrimino
            current_tetrimino = next_tetrimino
            next_tetrimino = Tetrimino()
            change_tetrimino = False
            
            # Clear rows and update score
            score = clear_rows(grid, score)
            
            # Check if game over
            if check_lost(grid):
                run = False
        
        screen.fill(BLACK)
        draw_grid(grid)
        draw_tetrimino(current_tetrimino)
        draw_next_shape(next_tetrimino)
        draw_score(score)
        pygame.display.update()
    
    # Game over message
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(f'Game Over! Final Score: {score}', 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - label.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds before closing

if __name__ == "__main__":
    main()
