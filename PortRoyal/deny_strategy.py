from enum import Enum

from PortRoyal.utils import Color
from PortRoyal.board import Board
from PortRoyal.roll import Roll


def deny_never():
    return False


def deny_always(swords: int, roll: Roll, rolls_left: bool) -> bool:
    if roll.get_swords() <= swords and rolls_left is True:
        return True
    else:
        return False


def deny_smart(swords: int, board: Board, roll: Roll, rolls_left: bool) -> bool:
    if roll.get_swords() <= swords and rolls_left is True:
        if roll.color == Color.BLACK:
            return True
        if roll.color in [Color.RED, Color.BLUE] and swords >= 4:
            if (roll.color == Color.RED
                    and board.ships.get(Color.BLUE) is not None
                    and board.ships.get(Color.BLACK) is not None):
                return False
            if (roll.color == Color.BLUE
                    and board.ships.get(Color.RED) is not None
                    and board.ships.get(Color.BLACK) is not None):
                return False
            if (roll.color == Color.BLUE
                    and board.ships.get(Color.RED) is not None
                    and board.ships.get(Color.BLACK) is not None):
                return False
            if (board.ships.get(Color.ORANGE) is None
                    or board.ships.get(Color.YELLOW) is None
                    or board.ships.get(Color.GREEN) is None):
                return True
    else:
        return False


class DenyStrategy(Enum):
    NEVER = deny_never
    ALWAYS = deny_always
    SMART = deny_smart
