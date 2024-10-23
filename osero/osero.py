import pygame
import sys

BOARD_SIZE = 8
CELL_SIZE = 50
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# オセロの盤面を初期化
def init_board():
    board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[3][3] = board[4][4] = BLACK
    board[3][4] = board[4][3] = WHITE
    return board


# 石を置ける位置を取得
def get_valid_moves(board, color):
    valid_moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] is None and is_valid_move(board, x, y, color):
                valid_moves.append((x, y))
    return valid_moves


# 石を置けるかチェック
def is_valid_move(board, x, y, color):
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return False
    if board[y][x] is not None:
        return False

    opponent_color = BLACK if color == WHITE else WHITE

    for dx, dy in [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]:
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < BOARD_SIZE
            and 0 <= ny < BOARD_SIZE
            and board[ny][nx] == opponent_color
        ):
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
                    break
                if board[ny][nx] == color:
                    return True
                if board[ny][nx] is None:
                    break

    return False


# 石を反転
def flip_discs(board, x, y, color):
    opponent_color = BLACK if color == WHITE else WHITE

    for dx, dy in [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]:
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < BOARD_SIZE
            and 0 <= ny < BOARD_SIZE
            and board[ny][nx] == opponent_color
        ):
            while True:
                nx += dx
                ny += dy
                if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
                    break
                if board[ny][nx] == color:
                    while True:
                        nx -= dx
                        ny -= dy
                        if nx == x and ny == y:
                            break
                        board[ny][nx] = color
                    break
                if board[ny][nx] is None:
                    break


# ゲームの状態を描画
def draw_board(screen, board, valid_moves, current_player, game_over, winner):
    screen.fill(GREEN)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[y][x] == BLACK:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 2 - 5,
                )
            elif board[y][x] == WHITE:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 2 - 5,
                )

    for x, y in valid_moves:
        pygame.draw.circle(
            screen,
            GREEN,
            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
            5,
        )

    # 次の駒の打ち手を表示
    if not game_over:
        font = pygame.font.Font(None, 36)
        text = font.render(
            "Next: " + ("Black" if current_player == BLACK else "White"), True, BLUE
        )
        screen.blit(text, (10, WINDOW_SIZE - 30))

    # 勝者を表示
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render(
            "Winner: " + ("Black" if winner == BLACK else "White"), True, RED
        )
        screen.blit(text, (WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 - 20))

    # 終了ボタンを表示
    if game_over:
        pygame.draw.rect(
            screen, RED, (WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 + 20, 100, 40)
        )
        text = font.render("Quit", True, WHITE)
        screen.blit(text, (WINDOW_SIZE // 2 - 20, WINDOW_SIZE // 2 + 30))


# ゲームのメイン処理
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Othello")

    board = init_board()
    current_player = BLACK
    font = pygame.font.Font(None, 36)
    game_over = False
    winner = None

    while True:
        valid_moves = get_valid_moves(board, current_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    x, y = event.pos
                    if (
                        WINDOW_SIZE // 2 - 50 <= x <= WINDOW_SIZE // 2 + 50
                        and WINDOW_SIZE // 2 + 20 <= y <= WINDOW_SIZE // 2 + 60
                    ):
                        pygame.quit()
                        sys.exit()
                elif valid_moves:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if (col, row) in valid_moves:
                        board[row][col] = current_player
                        flip_discs(board, col, row, current_player)
                        current_player = WHITE if current_player == BLACK else BLACK

        # ゲームの終了条件をチェック
        if not valid_moves:
            current_player = WHITE if current_player == BLACK else BLACK
            valid_moves = get_valid_moves(board, current_player)
            if not valid_moves:
                game_over = True
                black_count = sum(row.count(BLACK) for row in board)
                white_count = sum(row.count(WHITE) for row in board)
                if black_count > white_count:
                    winner = BLACK
                elif white_count > black_count:
                    winner = WHITE

        draw_board(screen, board, valid_moves, current_player, game_over, winner)
        pygame.display.flip()


if __name__ == "__main__":
    main()
