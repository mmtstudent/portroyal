from enum import Enum

from PortRoyal.board import Board
from PortRoyal.roll import Roll


def deny_never():
    return False


def deny_always(swords: int, board: Board, roll: Roll, rolls_left: int) -> bool:
    if roll.get_swords() <= swords and rolls_left > 1:
        return True
    else:
        return False


class DenyStrategy(Enum):
    NEVER = deny_never
    ALWAYS = deny_always
