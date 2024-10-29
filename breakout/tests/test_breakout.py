import sys
import os
import unittest
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from breakout import create_ball, reset_game

class TestBreakout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen_size = 600
        pygame.display.set_mode((cls.screen_size, cls.screen_size))

    def setUp(self):
        self.screen_size = 600

    def test_create_ball(self):
        ball = create_ball()
        
        # ボールの位置が画面中央にあることを確認
        self.assertEqual(ball['rect'].centerx, self.screen_size // 2)
        self.assertEqual(ball['rect'].centery, self.screen_size // 2)
        
        # ボールの速度が正しい範囲にあることを確認
        self.assertIn(ball['speed'][0], [-4, 4])  # initial_ball_speed
        self.assertEqual(ball['speed'][1], -4)    # initial_ball_speed
        
        # ボールのサイズが正しいことを確認
        self.assertEqual(ball['rect'].width, 20)  # ball_radius * 2
        self.assertEqual(ball['rect'].height, 20) # ball_radius * 2
        
        # ボールの初期速度を確認
        initial_ball = create_ball()
        initial_speed_x = abs(initial_ball['speed'][0])
        initial_speed_y = abs(initial_ball['speed'][1])
        
        # 複数回ボールを作成して速度が上がることを確認
        for _ in range(2):
            new_ball = create_ball()
            new_speed_x = abs(new_ball['speed'][0])
            new_speed_y = abs(new_ball['speed'][1])
            
            self.assertGreater(new_speed_x, initial_speed_x)
            self.assertGreater(new_speed_y, initial_speed_y)
            
            initial_speed_x = new_speed_x
            initial_speed_y = new_speed_y

    def test_reset_game(self):
        paddle, balls, blocks, score_counter = reset_game()
        
        # パドルの初期位置と大きさを確認
        self.assertEqual(paddle.width, 100)  # paddle_width
        self.assertEqual(paddle.height, 10)  # paddle_height
        self.assertEqual(paddle.bottom, self.screen_size - 20)  # screen_height - 30 + paddle_height
        self.assertEqual(paddle.centerx, self.screen_size // 2)
        
        # 初期状態でボールが1つ存在することを確認
        self.assertEqual(len(balls), 1)
        
        # スコアを増やしてボールが増えることを確認
        initial_balls = len(balls)
        for score in [1000, 2000, 3000, 4000]:  # スコアの閾値
            score_counter['score'] = score
            reset_game()
            self.assertEqual(len(balls), initial_balls + (score // 1000))
            
        # 最大ボール数を超えないことを確認
        score_counter['score'] = 10000
        reset_game()
        self.assertLessEqual(len(balls), 5)  # 最大ボール数
        
        # ブロックの数を確認（10x5=50個）
        self.assertEqual(len(blocks), 50)
        
        # 最初のブロックの位置とサイズを確認
        first_block = blocks[0]
        self.assertEqual(first_block.width, 60)   # block_width
        self.assertEqual(first_block.height, 20)  # block_height
        self.assertEqual(first_block.x, 5)        # block_margin
        self.assertEqual(first_block.y, 5)        # block_margin

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main() 