from PortRoyal.deny_strategy import DenyStrategy, deny_always, deny_never, deny_smart
from PortRoyal.roll import Roll
from PortRoyal.board import Board
from PortRoyal.utils import Color, Letter


class Player:

    def __init__(self,
                 points: int = 0,
                 skulls: int = 0,
                 swords: int = 0,
                 movement: int = 0,
                 deny_strategy: DenyStrategy = DenyStrategy.NEVER,
                 orange_wheels: int = 0,
                 blue_wheels: int = 0):
        self.skulls = skulls
        self.points = points
        self.blue_wheels = blue_wheels
        self.movement = movement
        self.swords = swords
        self.deny_strategy = deny_strategy
        self.orange_wheels = orange_wheels

    def will_deny(self, board: Board, roll: Roll, rolls_left: bool) -> bool:
        match self.deny_strategy:
            case DenyStrategy.SMART:
                return deny_smart(self.swords, board, roll, rolls_left)
            case DenyStrategy.ALWAYS:
                return deny_always(self.swords, roll, rolls_left)
            case DenyStrategy.NEVER:
                return deny_never()

