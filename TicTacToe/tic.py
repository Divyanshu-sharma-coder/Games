import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700  # Extra space for score display
LINE_COLOR = (23, 145, 135)  # Teal
BG_COLOR = (28, 28, 28)      # Dark gray
X_COLOR = (239, 71, 111)     # Red
O_COLOR = (6, 214, 160)      # Green
TEXT_COLOR = (255, 255, 255) # White
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
FONT = pygame.font.SysFont("Arial", 40)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Unbeatable Tic-Tac-Toe")

class TicTacToe:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.player_turn = True  # True = X (Player), False = O (AI)
        self.game_over = False
        self.x_score = 0
        self.o_score = 0
        self.winner = None

    def draw_grid(self):
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

    def draw_figures(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 1:  # X
                    pygame.draw.line(screen, X_COLOR, 
                                    (col * SQUARE_SIZE + 25, row * SQUARE_SIZE + 25),
                                    (col * SQUARE_SIZE + SQUARE_SIZE - 25, row * SQUARE_SIZE + SQUARE_SIZE - 25), 
                                    LINE_WIDTH)
                    pygame.draw.line(screen, X_COLOR,
                                    (col * SQUARE_SIZE + SQUARE_SIZE - 25, row * SQUARE_SIZE + 25),
                                    (col * SQUARE_SIZE + 25, row * SQUARE_SIZE + SQUARE_SIZE - 25), 
                                    LINE_WIDTH)
                elif self.board[row][col] == 2:  # O
                    pygame.draw.circle(screen, O_COLOR, 
                                      (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                      SQUARE_SIZE // 2 - 25, LINE_WIDTH)

    def check_win(self, player):
        # Check rows and columns
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(self.board[row][col] != 0 for row in range(3) for col in range(3))

    def minimax(self, board, depth, is_maximizing):
        if self.check_win(2):
            return 1
        if self.check_win(1):
            return -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = 0
                        best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = 0
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        if best_move:
            row, col = best_move
            self.board[row][col] = 2
            if self.check_win(2):
                self.winner = "O"
                self.o_score += 1
                self.game_over = True
            elif self.check_draw():
                self.game_over = True

    def draw_score(self):
        score_text = f"X: {self.x_score}  |  O: {self.o_score}"
        text_surface = FONT.render(score_text, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 80))

        if self.game_over:
            if self.winner:
                result_text = f"{self.winner} wins! Tap to restart."
            else:
                result_text = "Draw! Tap to restart."
            result_surface = FONT.render(result_text, True, TEXT_COLOR)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT - 40))

    def handle_click(self, pos):
        if not self.game_over and self.player_turn:
            col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
            if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == 0:
                self.board[row][col] = 1
                if self.check_win(1):
                    self.winner = "X"
                    self.x_score += 1
                    self.game_over = True
                elif self.check_draw():
                    self.game_over = True
                else:
                    self.player_turn = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        self.reset_game()
                    else:
                        if event.type == pygame.FINGERDOWN:
                            pos = (int(event.x * WIDTH), int(event.y * (HEIGHT - 100)))
                        else:
                            pos = event.pos
                        self.handle_click(pos)

            # AI move
            if not self.player_turn and not self.game_over:
                self.ai_move()
                self.player_turn = True

            # Draw everything
            screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_figures()
            self.draw_score()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
