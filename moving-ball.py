import pygame
import sys
import random
import os

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("敵を避けるゲーム")

# 色の設定
ball_color = (255, 0, 0)  # 赤色
enemy_color = (0, 255, 0)  # 緑色
item_color = (0, 0, 255)  # 青色

# プレイヤーの設定
ball_radius = 20
ball_x, ball_y = screen_width // 2, screen_height - 50
ball_speed = 5
player_rect = pygame.Rect(
    ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2
)

# 敵キャラの設定
enemy_width, enemy_height = 40, 40
enemy_speed = 3

# アイテムの設定
item_width, item_height = 20, 20
item_speed = 2
items = []

# フォントの設定
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# スコアの初期値
score = 0

# ハイスコアの初期化
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

# ゲームオーバー状態を管理するフラグ
game_over = False

# 敵キャラを管理するリスト
enemies = []


# 敵キャラを生成してリストに追加する関数
def create_enemy():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = 0
    enemies.append([enemy_x, enemy_y])


# アイテムを生成してリストに追加する関数
def create_item():
    item_x = random.randint(0, screen_width - item_width)
    item_y = 0
    items.append([item_x, item_y])


# ゲームオーバー画面を表示する関数
def show_game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 100))

    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    screen.blit(high_score_text, (screen_width // 2 - 100, screen_height // 2))

    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - 200, screen_height // 2 + 50))

    pygame.display.flip()


# 最初の敵キャラを3体作成
for _ in range(3):
    create_enemy()

# ゲームのメインループ
while True:
    if game_over:
        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))

        show_game_over_screen()

        # イベント処理（ゲームオーバー時）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # ゲームのリセット
                    ball_x, ball_y = screen_width // 2, screen_height - 50
                    player_rect.x = ball_x - ball_radius
                    player_rect.y = ball_y - ball_radius
                    enemies.clear()  # 敵キャラリストをクリア
                    items.clear()  # アイテムリストをクリア
                    for _ in range(3):  # 敵キャラを再生成
                        create_enemy()
                    score = 0
                    game_over = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        continue

    # イベント処理（通常時）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
        ball_x += ball_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
        ball_y += ball_speed

    # プレイヤーの位置を更新
    player_rect.x = ball_x - ball_radius
    player_rect.y = ball_y - ball_radius

    # 敵キャラの移動と衝突判定
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        enemy[1] += enemy_speed  # 敵キャラのy座標を移動
        if enemy[1] > screen_height:
            enemy[0] = random.randint(0, screen_width - enemy_width)
            enemy[1] = 0
            score += 1  # 敵を避けたらスコアを増やす

        if player_rect.colliderect(enemy_rect):
            game_over = True

    # アイテムの移動と衝突判定
    for item in items[:]:
        item_rect = pygame.Rect(item[0], item[1], item_width, item_height)
        item[1] += item_speed  # アイテムのy座標を移動
        if item[1] > screen_height:
            items.remove(item)  # アイテムが画面外に出たら削除
        elif player_rect.colliderect(item_rect):
            score += 5  # アイテムを取得したらスコアを増やす
            items.remove(item)  # アイテムを削除

    # 新しい敵キャラをランダムに追加
    if random.randint(1, 100) < 2:  # 2%の確率で新しい敵を追加
        create_enemy()

    # 新しいアイテムをランダムに追加
    if random.randint(1, 100) < 3:  # 3%の確率で新しいアイテムを追加
        create_item()

    # 画面を黒で塗りつぶす
    screen.fill((0, 0, 0))

    # ボール（プレイヤー）を三角形で描画
    player_points = [
        (ball_x, ball_y - ball_radius),  # 上頂点
        (ball_x - ball_radius, ball_y + ball_radius),  # 左下
        (ball_x + ball_radius, ball_y + ball_radius),  # 右下
    ]
    pygame.draw.polygon(screen, ball_color, player_points)

    # 敵キャラを楕円形で描画
    for enemy in enemies:
        pygame.draw.ellipse(
            screen, enemy_color, (enemy[0], enemy[1], enemy_width, enemy_height)
        )

    # アイテムを円形で描画
    for item in items:
        pygame.draw.circle(
            screen,
            item_color,
            (item[0] + item_width // 2, item[1] + item_height // 2),
            item_width // 2,
        )

    # スコアを描画
    score_text = font.render(
        f"Score: {score}", True, (255, 255, 255)
    )  # 白色でスコア表示
    screen.blit(score_text, (10, 10))  # 画面左上に表示

    # ハイスコアを描画
    high_score_text = font.render(
        f"High Score: {high_score}", True, (255, 255, 0)
    )  # 黄色でハイスコア表示
    screen.blit(high_score_text, (10, 50))  # スコアの下に表示

    # 画面更新
    pygame.display.flip()

    # フレームレートの設定
    pygame.time.Clock().tick(60)
