import pygame
import sys

# 定数の設定
ROW_COUNT = 6
COLUMN_COUNT = 7
CELL_SIZE = 100
RADIUS = int(CELL_SIZE / 2 - 5)
WINDOW_WIDTH = COLUMN_COUNT * CELL_SIZE
WINDOW_HEIGHT = (ROW_COUNT + 1) * CELL_SIZE

# 色の定義
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# ボードを初期化
def create_board():
    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    return board

# ボードを描画
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * CELL_SIZE, r * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * CELL_SIZE + CELL_SIZE / 2), int(r * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * CELL_SIZE + CELL_SIZE / 2), WINDOW_HEIGHT - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * CELL_SIZE + CELL_SIZE / 2), WINDOW_HEIGHT - int(r * CELL_SIZE + CELL_SIZE / 2)), RADIUS)
    pygame.display.update()

# 有効な列を取得
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# 次の空いている行を取得
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# ボードに駒を落とす
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# 勝利条件をチェック
def winning_move(board, piece):
    # 横方向のチェック
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # 縦方向のチェック
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # 斜め方向のチェック（右上がり）
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # 斜め方向のチェック（右下がり）
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# ゲームのメイン処理
def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Four in a Row")
    board = create_board()
    draw_board(board)
    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(CELL_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(CELL_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                # プレイヤー1のターン
                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx / CELL_SIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                            font = pygame.font.SysFont("monospace", 75)
                            label = font.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                # プレイヤー2のターン
                else:
                    posx = event.pos[0]
                    col = int(posx / CELL_SIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                            font = pygame.font.SysFont("monospace", 75)
                            label = font.render("Player 2 wins!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

if __name__ == "__main__":
    main()

