import unittest
from unittest.mock import patch

from PortRoyal.game import Game
from PortRoyal.board import Board
from PortRoyal.player import Player
from PortRoyal.roll import Roll, roll_dice
from PortRoyal.utils import Letter, Color


class TestGame(unittest.TestCase):

    def test_roll_for_turn_ship(self):
        game = Game(board=Board(), player=Player())

        roll = Roll(color=Color.YELLOW, letter=Letter.A)

        result = game.roll_for_turn(roll=roll, rolls_left=3)

        self.assertFalse(result)
        self.assertIn(Color.YELLOW, game.board.ships)
        self.assertEqual(game.board.ships[Color.YELLOW], [Letter.A])

    def test_roll_for_turn_wheel(self):
        game = Game(board=Board(), player=Player())

        roll = Roll(color=Color.RED, letter=Letter.E)

        failed = game.roll_for_turn(roll=roll, rolls_left=3)

        self.assertFalse(failed)
        self.assertIn(Color.RED, game.board.wheels)
        self.assertEqual(game.board.wheels[Color.RED], [Letter.E])

    @patch('PortRoyal.game.roll_dice')
    def test_roll_to_x_ships_success(self, mock_roll_dice):
        game = Game(board=Board(), player=Player())

        mock_roll_dice.side_effect = [
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.ORANGE),
            Roll(letter=Letter.A, color=Color.YELLOW)
        ]

        # Test with the number of ships to roll to
        target_ships = 3
        success = game.roll_to_x_ships(target_ships)

        self.assertTrue(success)
        self.assertEqual(game.board.count_ships(), target_ships)

    @patch('PortRoyal.game.roll_dice')
    def test_roll_to_x_ships_fail(self, mock_roll_dice):
        game = Game(board=Board(), player=Player())

        mock_roll_dice.side_effect = [
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.YELLOW)
        ]

        # Test with the number of ships to roll to
        target_ships = 3
        success = game.roll_to_x_ships(target_ships)

        self.assertFalse(success)

    @patch('PortRoyal.game.roll_dice')
    def test_roll_to_x_items_success(self, mock_roll_dice):
        game = Game(board=Board(), player=Player())

        mock_roll_dice.side_effect = [
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.ORANGE),
            Roll(letter=Letter.A, color=Color.YELLOW)
        ]

        # Test with the number of ships to roll to
        target_ships = 3
        success = game.roll_to_x_ships(target_ships)

        self.assertTrue(success)
        self.assertEqual(game.board.count_ships(), target_ships)

    @patch('PortRoyal.game.roll_dice')
    def test_roll_to_x_items_fail(self, mock_roll_dice):
        game = Game(board=Board(), player=Player())

        mock_roll_dice.side_effect = [
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.BLUE),
            Roll(letter=Letter.A, color=Color.YELLOW)
        ]

        # Test with the number of ships to roll to
        target_ships = 3
        success = game.roll_to_x_items(target_ships)

        self.assertFalse(success)
