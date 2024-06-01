import unittest

from PortRoyal.board import Board
from PortRoyal.utils import Color, Letter


class TestBoard(unittest.TestCase):
    def test_initialization(self):
        # Test default initialization
        board = Board()
        self.assertFalse(board.ships[Color.BLUE])
        self.assertFalse(board.ships[Color.ORANGE])
        self.assertFalse(board.ships[Color.YELLOW])
        self.assertFalse(board.ships[Color.RED])
        self.assertFalse(board.ships[Color.BLACK])
        self.assertFalse(board.ships[Color.GREEN])

        self.assertFalse(board.wheels[Color.BLUE])
        self.assertFalse(board.wheels[Color.ORANGE])
        self.assertFalse(board.wheels[Color.YELLOW])
        self.assertFalse(board.wheels[Color.RED])
        self.assertFalse(board.wheels[Color.GREEN])

    def test_custom_initialization(self):
        # Test custom initialization
        board = Board(blue_ship=Letter.A, red_wheel=Letter.E)
        self.assertTrue(board.ships[Color.BLUE])
        self.assertFalse(board.ships[Color.ORANGE])
        self.assertFalse(board.ships[Color.YELLOW])
        self.assertFalse(board.ships[Color.RED])
        self.assertFalse(board.ships[Color.BLACK])
        self.assertFalse(board.ships[Color.GREEN])

        self.assertTrue(board.wheels[Color.RED])
        self.assertFalse(board.wheels[Color.BLUE])
        self.assertFalse(board.wheels[Color.ORANGE])
        self.assertFalse(board.wheels[Color.YELLOW])
        self.assertFalse(board.wheels[Color.GREEN])

    def test_count_items(self):
        board = Board(blue_ship=Letter.A, orange_wheel=Letter.E)
        assert board.count_items() == 2
