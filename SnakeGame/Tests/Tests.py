import unittest
from unittest.mock import MagicMock
from snake_game import Snake, Food, Game, User

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.canvas = MagicMock()
        self.snake = Snake(self.canvas)

    def test_initialize_snake(self):
        self.assertEqual(len(self.snake.coordinates), 3)
        self.assertEqual(len(self.snake.squares), 3)

    def test_move(self):
        initial_length = len(self.snake.coordinates)
        self.snake.move()
        self.assertEqual(len(self.snake.coordinates), initial_length + 1)

    def test_remove_tail(self):
        initial_length = len(self.snake.coordinates)
        self.snake.remove_tail()
        self.assertEqual(len(self.snake.coordinates), initial_length - 1)

    def test_change_direction(self):
        initial_direction = self.snake.direction
        self.snake.change_direction('up')
        self.assertEqual(self.snake.direction, 'up')
        self.snake.change_direction('down')
        self.assertEqual(self.snake.direction, 'up')  # should not change if opposite direction
        self.snake.change_direction('left')
        self.assertEqual(self.snake.direction, 'left')
        self.snake.change_direction('right')
        self.assertEqual(self.snake.direction, 'left')  # should not change if opposite direction

class TestFood(unittest.TestCase):
    def setUp(self):
        self.canvas = MagicMock()
        self.food = Food(self.canvas)

    def test_initialize_food(self):
        self.assertTrue(self.food.coordinates)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.window = MagicMock()
        self.canvas = MagicMock()
        self.user = MagicMock()
        self.game = Game(self.window, self.canvas, self.user)

    def test_check_collision(self):
        # Test collision with walls
        self.game.snake.coordinates[0] = [-10, 0]
        self.assertTrue(self.game.check_collision())

        # Reset snake position
        self.game.snake.coordinates[0] = [0, 0]

        # Test collision with itself
        self.game.snake.coordinates = [[0, 0], [0, 50], [0, 100], [0, 0]]
        self.assertTrue(self.game.check_collision())

        # Reset snake position
        self.game.snake.coordinates = [[0, 0]]

        # Test no collision
        self.assertFalse(self.game.check_collision())

if __name__ == '__main__':
    unittest.main()
