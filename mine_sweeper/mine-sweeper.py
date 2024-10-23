import pygame
import sys
import random

# 定数の設定
BOARD_SIZE = 10
CELL_SIZE = 40
NUM_MINES = 10
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# マインスイーパーの盤面を初期化
def init_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    mines = set()
    while len(mines) < NUM_MINES:
        x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[y][x] = -1
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] != -1:
                        board[ny][nx] += 1
    return board

# ゲームの状態を描画
def draw_board(screen, board, revealed, flags):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[y][x]:
                pygame.draw.rect(screen, WHITE, rect)
                if board[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[y][x]), True, BLACK)
                    screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if flags[y][x]:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            pygame.draw.rect(screen, BLACK, rect, 1)

# ゲームのメイン処理
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Mine Sweeper")

    # Define these variables in the outer scope
    board = None
    revealed = None
    flags = None
    game_over = False
    game_won = False

    def reset_game():
        nonlocal board, revealed, flags, game_over, game_won
        board = init_board()
        revealed = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        flags = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        game_over = False
        game_won = False

    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not game_won:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if event.button == 1:  # 左クリック
                    if board[row][col] == -1:
                        game_over = True
                    else:
                        revealed[row][col] = True
                elif event.button == 3:  # 右クリック
                    flags[row][col] = not flags[row][col]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'R'キーでリトライ
                    reset_game()

        # クリア判定
        if not game_over and all(
            (revealed[y][x] or board[y][x] == -1) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)
        ):
            game_won = True

        screen.fill(GREEN)
        draw_board(screen, board, revealed, flags)

        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over", True, RED)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            screen.blit(text, text_rect)

            retry_text = font.render("Press 'R' to Retry", True, RED)
            retry_text_rect = retry_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 80))
            screen.blit(retry_text, retry_text_rect)
        elif game_won:
            font = pygame.font.Font(None, 72)
            text = font.render("You Win!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
