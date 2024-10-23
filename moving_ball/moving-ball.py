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
enemy_color = (0, 255, 0)  # 緑色
item_color = (0, 0, 255)  # 青色

# プレイヤーの設定
ball_radius = 20
ball_x, ball_y = screen_width // 2, screen_height - 50
ball_speed = 5

# プレイヤーの画像を読み込む
current_directory = os.path.dirname(__file__)
player_image_path = os.path.join(current_directory, "player.webp")
player_image = pygame.image.load(player_image_path).convert_alpha()
player_image = pygame.transform.scale(player_image, (ball_radius * 2, ball_radius * 2))
player_rect = player_image.get_rect(center=(ball_x, ball_y))

# 敵キャラの設定
enemy_width, enemy_height = 40, 40
enemy_speed = 3

# アイテムの設定
item_width, item_height = 20, 20
item_speed = 2
items = []

# フォントの設定
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"  # 日本語フォントファイルのパスを指してください
font_size = 18
try:
    font = pygame.font.Font(font_path, font_size)
    game_over_font = pygame.font.Font(font_path, 36)
except FileNotFoundError:
    print(f"フォントファイル '{font_path}' が見つかりません。")
    pygame.quit()
    sys.exit()

# スコアの初期値
score = 0


# ランキングの初期化
def load_rankings():
    rankings = []
    current_directory = os.path.dirname(__file__)
    ranking_file_path = os.path.join(current_directory, "ranking.txt")
    if os.path.exists(ranking_file_path):
        with open(ranking_file_path, "r") as f:
            for line in f:
                if line.strip():
                    name, score_str = line.strip().split(",")
                    rankings.append((name, int(score_str)))
    return rankings


def save_rankings(rankings):
    current_directory = os.path.dirname(__file__)
    ranking_file_path = os.path.join(current_directory, "ranking.txt")
    with open(ranking_file_path, "w") as f:
        for name, score in rankings[:5]:
            f.write(f"{name},{score}\n")


rankings = load_rankings()

# ゲームの状態を管理する変数
game_state = "start"  # 'start', 'playing', 'game_over', 'entering_name'
player_name = ""

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


# スタート画面を表示する関数
def show_start_screen():
    screen.fill((0, 0, 0))
    title_text = game_over_font.render("敵を避けるゲーム", True, (255, 255, 255))
    instruction_text = font.render(
        "スペースキーを押してスタート", True, (255, 255, 255)
    )
    rules_text1 = font.render(
        "ルール：敵を避けてスコアを稼ごう！", True, (255, 255, 255)
    )
    rules_text2 = font.render(
        "矢印キーで移動、アイテムを取るとスコアアップ！", True, (255, 255, 255)
    )
    screen.blit(title_text, (screen_width // 2 - 200, screen_height // 2 - 150))
    screen.blit(rules_text1, (screen_width // 2 - 200, screen_height // 2 - 50))
    screen.blit(rules_text2, (screen_width // 2 - 200, screen_height // 2))
    screen.blit(instruction_text, (screen_width // 2 - 150, screen_height // 2 + 100))
    pygame.display.flip()


# ゲームオーバー画面を表示する関数
def show_game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("ゲームオーバー", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 150))

    # ランキングを表示
    rank_text = font.render("ランキング：", True, (255, 255, 255))
    screen.blit(rank_text, (screen_width // 2 - 80, screen_height // 2 - 80))
    for i, (name, s) in enumerate(rankings):
        ranking_text = font.render(f"{i+1}. {name}: {s}", True, (255, 255, 0))
        screen.blit(
            ranking_text, (screen_width // 2 - 100, screen_height // 2 - 50 + i * 30)
        )

    restart_text = font.render(
        "スペースキーでスタート画面に戻る / Qキーで終了", True, (255, 255, 255)
    )
    screen.blit(restart_text, (screen_width // 2 - 250, screen_height // 2 + 100))

    pygame.display.flip()


# 名前入力画面を表示する関数
def show_name_input_screen(player_name):
    screen.fill((0, 0, 0))
    prompt_text = font.render("あなたの名前を入力してください：", True, (255, 255, 255))
    screen.blit(prompt_text, (screen_width // 2 - 200, screen_height // 2 - 50))
    name_text = font.render(player_name, True, (255, 255, 255))
    screen.blit(name_text, (screen_width // 2 - 100, screen_height // 2))
    pygame.display.flip()


# 最初の敵キャラを3体作成
for _ in range(3):
    create_enemy()

# ゲームのメインループ
while True:
    if game_state == "start":
        # スタート画面の処理
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "playing"
                    # ゲームの初期化
                    ball_x, ball_y = screen_width // 2, screen_height - 50
                    player_rect.center = (ball_x, ball_y)
                    enemies.clear()
                    items.clear()
                    for _ in range(3):
                        create_enemy()
                    score = 0
        pygame.display.flip()
        continue

    elif game_state == "playing":
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
        player_rect.center = (ball_x, ball_y)

        # 敵キャラの移動と衝突判定
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            enemy[1] += enemy_speed
            if enemy[1] > screen_height:
                enemy[0] = random.randint(0, screen_width - enemy_width)
                enemy[1] = 0
                score += 1

            if player_rect.colliderect(enemy_rect):
                # ゲームオーバー状態に移行
                if len(rankings) < 5 or score > rankings[-1][1]:
                    game_state = "entering_name"
                    player_name = ""
                else:
                    game_state = "game_over"

        # アイテムの移動と衝突判定
        for item in items[:]:
            item_rect = pygame.Rect(item[0], item[1], item_width, item_height)
            item[1] += item_speed
            if item[1] > screen_height:
                items.remove(item)
            elif player_rect.colliderect(item_rect):
                score += 5
                items.remove(item)

        # 新しい敵キャラをランダムに追加
        if random.randint(1, 100) < 2:
            create_enemy()

        # 新しいアイテムをランダムに追加
        if random.randint(1, 100) < 3:
            create_item()

        # 画面を黒で塗りつぶす
        screen.fill((0, 0, 0))

        # プレイヤーを描画
        screen.blit(player_image, player_rect)

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

        # スコアとハイスコアを描画（横並び）
        score_text = font.render(f"スコア: {score}", True, (255, 255, 255))
        if rankings:
            high_score_value = rankings[0][1]
        else:
            high_score_value = 0
        high_score_text = font.render(
            f"ハイスコア: {high_score_value}", True, (255, 255, 0)
        )
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (score_text.get_width() + 20, 10))

        # 画面更新
        pygame.display.flip()

        # フレームレートの設定
        pygame.time.Clock().tick(60)

    elif game_state == "entering_name":
        # 名前入力画面の処理
        show_name_input_screen(player_name)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    # 名前の入力が完了したらランキングに追加
                    if player_name == "":
                        player_name = "名無し"
                    rankings.append((player_name, score))
                    rankings.sort(key=lambda x: x[1], reverse=True)
                    rankings = rankings[:5]
                    save_rankings(rankings)
                    game_state = "game_over"
                elif len(player_name) < 10:
                    player_name += event.unicode
        pygame.display.flip()

    elif game_state == "game_over":
        # ゲームオーバー画面の処理
        show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # スタート画面に戻る
                    game_state = "start"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
