import pygame
import sys
import random

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygameのアイテム追加ゲーム")

# ボール（プレイヤー）の設定
ball_color = (255, 0, 0)  # 赤色
ball_radius = 20
ball_x, ball_y = screen_width // 2, screen_height - 50
ball_speed = 5

# 敵キャラの設定
enemy_color = (0, 255, 0)  # 緑色
enemy_width, enemy_height = 40, 40
enemy_speed = 3

# アイテムの設定
item_color = (0, 0, 255)  # 青色
item_width, item_height = 20, 20
item_speed = 2
items = []

# フォントの設定
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# スコアの初期値
score = 0

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
    screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))

    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - 200, screen_height // 2 + 50))

    pygame.display.flip()


# 最初の敵キャラを3体作成
for _ in range(3):
    create_enemy()

# ゲームのメインループ
while True:
    if game_over:
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
    if keys[pygame.K_LEFT] and ball_x - ball_radius > 0:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] and ball_x + ball_radius < screen_width:
        ball_x += ball_speed
    if keys[pygame.K_UP] and ball_y - ball_radius > 0:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN] and ball_y + ball_radius < screen_height:
        ball_y += ball_speed

    # 敵キャラの移動と衝突判定
    for enemy in enemies:
        enemy[1] += enemy_speed  # 敵キャラのy座標を移動
        if enemy[1] > screen_height:
            enemy[0] = random.randint(0, screen_width - enemy_width)
            enemy[1] = 0
            score += 1  # 敵を避けたらスコアを増やす

        # 衝突判定（プレイヤーと敵の距離が近い場合）
        if (ball_x - enemy[0]) ** 2 + (ball_y - enemy[1]) ** 2 < (
            ball_radius + enemy_width // 2
        ) ** 2:
            game_over = True

    # アイテムの移動
    for item in items:
        item[1] += item_speed  # アイテムのy座標を移動
        if item[1] > screen_height:
            items.remove(item)  # アイテムが画面外に出たら削除

        # アイテムの衝突判定（プレイヤーとアイテムの距離が近い場合）
        if (ball_x - item[0]) ** 2 + (ball_y - item[1]) ** 2 < (
            ball_radius + item_width // 2
        ) ** 2:
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

    # ボール（プレイヤー）を描画
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # 敵キャラを描画
    for enemy in enemies:
        pygame.draw.rect(
            screen, enemy_color, (enemy[0], enemy[1], enemy_width, enemy_height)
        )

    # アイテムを描画
    for item in items:
        pygame.draw.rect(
            screen, item_color, (item[0], item[1], item_width, item_height)
        )

    # スコアを描画
    score_text = font.render(
        f"Score: {score}", True, (255, 255, 255)
    )  # 白色でスコア表示
    screen.blit(score_text, (10, 10))  # 画面左上に表示

    # 画面更新
    pygame.display.flip()

    # フレームレートの設定
    pygame.time.Clock().tick(60)
