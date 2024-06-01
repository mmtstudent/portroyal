from PortRoyal.board import Board
from PortRoyal.player import Player
from PortRoyal.roll import Roll, roll_dice


class Game:
    board: Board
    player: Player

    def __init__(self,
                 board: Board,
                 player: Player
                 ):
        self.player = player
        self.board = board

    def roll_for_turn(self, roll: Roll, rolls_left: int) -> bool:
        if roll.is_wheel():
            if self.board.wheels.get(roll.color) is None:
                self.board.wheels[roll.color] = [roll.letter]
            else:
                if roll.get_swords() > self.player.swords:
                    self.board.wheels[roll.color] = None
        # Roll is Ship
        else:
            # Color is free
            if self.board.ships.get(roll.color) is None:
                # if you can't or don't want to deny -> take ship
                if not self.player.will_deny(self.board, roll, rolls_left):
                    self.board.ships[roll.color] = [roll.letter]
            # A ship of that color is already on the board
            else:
                if roll.get_swords() <= self.player.swords:
                    return False
                if self.player.orange_wheels > 0 and roll.get_swords() <= self.player.swords + 2:
                    # Deny and use orange wheel
                    self.player.orange_wheels -= 1
                elif self.player.orange_wheels > 1 and roll.get_swords() <= self.player.swords + 4:
                    # Deny and use 2 orange wheels
                    self.player.orange_wheels -= 2
                elif self.player.blue_wheels > 0:
                    # Use Blue wheel to re-roll color
                    self.player.blue_wheels -= 1
                    roll = roll_dice(roll.letter)
                    return self.roll_for_turn(roll, rolls_left)
                else:
                    return True
        return False

    def roll_to_x_items(self, x: int) -> bool:
        failed = False
        while self.board.count_items() < x and failed is False:
            roll = roll_dice()
            failed = self.roll_for_turn(roll, x - self.board.count_items())
        return not failed

    def roll_to_x_ships(self, x: int) -> bool:
        while self.board.count_ships() < x:
            roll = roll_dice()
            failed = self.roll_for_turn(roll, x - self.board.count_items())
            if failed:
                return False
        return True

    def roll_to_x(self, roll_to: int, count_wheels: bool) -> bool:
        if count_wheels:
            return self.roll_to_x_items(roll_to)
        else:
            return self.roll_to_x_ships(roll_to)
