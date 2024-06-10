from PortRoyal.board import Board
from PortRoyal.player import Player
from PortRoyal.roll import Roll, roll_dice
from PortRoyal.maps import Map, Map4


class Game:
    board: Board
    player: Player
    map: Map

    def __init__(self,
                 board: Board,
                 player: Player
                 ):
        self.player = player
        self.board = board
        self.map = Map4()

    def roll_for_turn(self, roll: Roll, rolls_left: bool) -> bool:
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
            rolls_left = x - self.board.count_items() > 1
            failed = self.roll_for_turn(roll, rolls_left)
        return not failed

    def roll_to_x_ships(self, x: int) -> bool:
        while self.board.count_ships() < x:
            roll = roll_dice()
            rolls_left = x - self.board.count_items() > 1
            failed = self.roll_for_turn(roll, rolls_left)
            if failed:
                return False
        return True

    def roll_to_x(self, roll_to: int, count_wheels: bool) -> bool:
        if count_wheels:
            return self.roll_to_x_items(roll_to)
        else:
            return self.roll_to_x_ships(roll_to)

    def roll_smart(self) -> bool:
        if self.player.swords > 4:
            while self.board.count_items() < 3:
                roll = roll_dice()
                failed = self.roll_for_turn(roll, True)
                if failed:
                    return False
            if self.board.count_wheels() > 0:
                failed = self.roll_to_x_items(5)
                if failed:
                    return False
            if self.board.count_wheels() >= 3:
                failed = self.roll_to_x_items(6)
                if failed:
                    return False
        return True

    def play_turn(self):
        self.roll_smart()
        return 0

    def play_game(self) -> int:
        rounds_played = 0
        while self.player.points > 11:
            self.play_turn()
            rounds_played += 1
        return rounds_played
