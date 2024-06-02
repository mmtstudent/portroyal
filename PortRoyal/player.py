from PortRoyal.deny_strategy import DenyStrategy, deny_always, deny_never, deny_smart
from PortRoyal.roll import Roll
from PortRoyal.board import Board
from PortRoyal.utils import Color, Letter


class Player:

    def __init__(self,
                 swords: int = 0,
                 movement: int = 0,
                 deny_strategy: DenyStrategy = DenyStrategy.NEVER,
                 orange_wheels: int = 0,
                 blue_wheels: int = 0):
        self.blue_wheels = blue_wheels
        self.movement = movement
        self.swords = swords
        self.deny_strategy = deny_strategy
        self.orange_wheels = orange_wheels

    def evaluate_board(self, board: Board) -> (int, int):
        free_spots = 0
        bad_spots = 0
        for ship in board.ships:
            # Color is open
            if not ship.value:
                if ship.name in (Color.GREEN, Color.YELLOW, Color.ORANGE):
                    free_spots += 3
                if ship.name in (Color.BLUE, Color.RED):
                    free_spots += 4
                if ship.name in Color.BLACK:
                    free_spots += 5
            # Color is used
            else:
                for letter in list(Letter):
                    roll = Roll(letter=letter, color=ship.name)
                    if roll.get_swords() > self.swords:
                        bad_spots += 1
        return free_spots, bad_spots

    def will_deny(self, board: Board, roll: Roll, rolls_left: int) -> bool:
        match self.deny_strategy:
            case DenyStrategy.SMART:
                return deny_smart(self.swords, board, roll, rolls_left)
            case DenyStrategy.ALWAYS:
                return deny_always(self.swords, roll, rolls_left)
            case DenyStrategy.NEVER:
                return deny_never()

    def calculate_swords_from_movement(self):
        # +5 from diplomat before 5.
        # no treasures
        if self.movement > 39:
            self.swords = 5
        elif self.movement >= 30:
            self.swords = 4
        elif self.movement >= 12:
            self.swords = 2
        else:
            self.swords = 0
