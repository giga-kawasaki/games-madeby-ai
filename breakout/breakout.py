import pygame
import sys
import random
import math

# 初期化
pygame.init()

# 画面サイズ
screen_size = 600
screen_width = screen_size
screen_height = screen_size

# テスト実行時はダミーの画面を使用
if 'pytest' in sys.modules:
    screen = pygame.Surface((screen_width, screen_height))
else:
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("ブロック崩し")

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# パドルの設定
paddle_width = 100
paddle_height = 10

# ボールの設定
ball_radius = 10
initial_ball_speed = 4
max_ball_speed = 8
speed_increase = 0.1
max_balls = 5  # 最大ボール数
balls_add_interval = 30  # ボールを追加する間隔（秒）

# ブロックの設定
block_width = 60
block_height = 20
block_margin = 5

def create_ball():
    return {
        'rect': pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2),
        'speed': [random.choice([-initial_ball_speed, initial_ball_speed]), -initial_ball_speed]
    }

def reset_game():
    global paddle, balls, blocks, last_ball_add_time
    paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)
    balls = [create_ball()]
    blocks = [pygame.Rect(block_margin + i * (block_width + block_margin),
                          block_margin + j * (block_height + block_margin),
                          block_width, block_height)
              for i in range(10) for j in range(5)]
    last_ball_add_time = pygame.time.get_ticks()

reset_game()

# ゲームループ
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.move_ip(6, 0)

    # ボールの移動と衝突判定
    for ball in balls[:]:
        ball['rect'].move_ip(ball['speed'])
        if ball['rect'].left <= 0 or ball['rect'].right >= screen_width:
            ball['speed'][0] = -ball['speed'][0]
        if ball['rect'].top <= 0:
            ball['speed'][1] = -ball['speed'][1]
        if ball['rect'].colliderect(paddle):
            ball['speed'][1] = -ball['speed'][1]

        # ブロックとの衝突
        for block in blocks[:]:
            if ball['rect'].colliderect(block):
                ball['speed'][1] = -ball['speed'][1]
                blocks.remove(block)

                # ボールの速度を増加
                current_ball_speed = min(math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2) + speed_increase, max_ball_speed)
                ball['speed'][0] = math.copysign(current_ball_speed / math.sqrt(2), ball['speed'][0])
                ball['speed'][1] = math.copysign(current_ball_speed / math.sqrt(2), ball['speed'][1])

        # ボールが画面外に出たらゲームオーバー
        if ball['rect'].bottom >= screen_height:
            balls.clear()  # すべてのボールを削除
            break  # ループを抜ける

    # 新しいボールの追加
    if current_time - last_ball_add_time > balls_add_interval * 1000 and len(balls) < max_balls:
        balls.append(create_ball())
        last_ball_add_time = current_time

    # 画面の更新
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, red, ball['rect'])
    for block in blocks:
        pygame.draw.rect(screen, white, block)
    pygame.display.flip()

    # ゲームオーバー
    if len(balls) == 0:
        # リトライメッセージを表示
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over! Press R to Retry", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()

        # リトライ待ち
        retry = False
        while not retry:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    retry = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        retry = True

    pygame.time.delay(30)

pygame.quit()
sys.exit()
