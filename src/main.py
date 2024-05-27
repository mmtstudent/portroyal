from dataclasses import dataclass

import random


@dataclass
class Board:
    board_ships: {}
    board_wheels: {}
    is_failed: bool = False

    @property
    def value(self):
        if self.is_failed:
            return 1
        value_list = []
        for item in self.board_ships:
            value_list.append(TwoDice(item, self.board_ships[item][0]).value)
        for item in self.board_wheels:
            value_list.append(TwoDice(item, self.board_wheels[item][0]).value)
        value_list.sort()
        take_x = max(len(value_list) - 3, 1)
        return sum(value_list[-take_x:])


@dataclass
class DiceValue:
    movement: int
    skulls: int

    @property
    def value(self) -> float:
        return self.movement - self.skulls * 0.75


@dataclass
class TwoDice:
    color: str
    letter: chr

    @property
    def swords(self) -> int:
        sum_swords = 0
        match self.letter:
            case 'a':
                sum_swords += 1
            case 'b':
                sum_swords += 2
            case 'c':
                sum_swords += 3
            case 'd':
                sum_swords += 4
            case 'e':
                sum_swords += 5

        match self.color:
            case 'black':
                sum_swords += 3
            case 'red' | 'blue':
                sum_swords += 2
            case 'green' | 'orange':
                sum_swords += 1
            case 'yellow':
                sum_swords += 0

        return sum_swords

    @property
    def is_wheel(self) -> bool:
        return (
                (self.color in ('yellow', 'green', 'orange') and self.letter in ['d', 'e'])
                or (self.color in ('red', 'blue') and self.letter in ['e']))

    @property
    def value(self) -> float:
        if self.is_wheel:
            # todo - how much is a wheel worth?
            match self.color:
                case 'yellow' | 'red' | 'orange' | 'green' | 'blue':
                    return 1.5
        else:
            match self.letter:
                case 'a':
                    return 1
                case 'b':
                    return 2
                case 'c' | 'd':
                    return 3
                case 'e':
                    return 4

    @property
    def skulls(self):
        if self.is_wheel:
            return 0
        else:
            match self.color, self.letter:
                case ('black' | 'red' | 'blue', 'c'):
                    return 1
                case ('black', 'e'):
                    return 2
                case _:
                    return 0


def roll_color():
    return random.choice(['red', 'green', 'blue', 'black', 'yellow', 'orange'])


def roll_letter():
    return random.choice(['a', 'b', 'b', 'c', 'd', 'e'])


class Game:
    rerolled_letter: chr = None

    def __init__(self, game_swords: int, game_blue_wheels: int, game_orange_wheels: int):
        self.swords = game_swords
        self.blue_wheels = game_blue_wheels
        self.orange_wheels = game_orange_wheels
        self.board = Board(board_ships={}, board_wheels={})

    def roll_dice(self, board: Board):
        roll = TwoDice(roll_color(), roll_letter())
        if self.rerolled_letter:
            roll = TwoDice(roll.color, self.rerolled_letter)
            self.rerolled_letter = None
        if roll.is_wheel:
            if roll.color not in board.board_wheels:
                board.board_wheels[roll.color] = [roll.letter]
            else:
                if roll.swords > self.swords:
                    del board.board_wheels[roll.color]
        else:
            if roll.color not in board.board_ships:
                board.board_ships[roll.color] = [roll.letter]
            else:
                if roll.swords > self.swords:
                    if self.orange_wheels > 0 and roll.swords < self.swords + 2:
                        # Deny and use orange wheel
                        self.orange_wheels -= 1
                    if self.orange_wheels > 0 and roll.swords < self.swords + 4:
                        # Deny and use orange wheel
                        self.orange_wheels -= 2
                    elif self.blue_wheels > 0:
                        # Use Blue wheel to re-roll color
                        self.blue_wheels -= 1
                        self.rerolled_letter = roll.letter
                    else:
                        board.is_failed = True
        return board

    def roll_to_min_x(self, x: int):
        while len(self.board.board_ships) < x and len(self.board.board_wheels) + len(self.board.board_ships) < 6:
            board = self.roll_dice(self.board)
            if board.is_failed:
                return 0, board.value
        return 1, self.board.value

    def roll_to_x(self, x: int):
        board = Board(board_ships={}, board_wheels={})
        while len(board.board_ships) + len(board.board_wheels) < x:
            board = self.roll_dice(board)
            if board.is_failed:
                return 0, board.value
        return 1, board.value


if __name__ == '__main__':
    rolls = 100000
    roll_to = 7
    swords = 5
    blue_wheels = 2
    orange_wheels = 0
    # Success rate - avg Value
    # 5 total = 29% - 2.19
    # 3 ships = 55% - 2.21
    # Finish with 5 swords -> 47%
    # blue wheels   -> 1: 71% -> 2: 85%
    # orange wheels -> 1: 64% -> 2: 76%
    # orange&blue 1 -> 77%

    did_succeed = []
    board_values = []
    for i in range(0, rolls):
        game = Game(game_swords=swords, game_blue_wheels=blue_wheels, game_orange_wheels=orange_wheels)
        #success, board_value = game.roll_to_min_x(roll_to)
        success, board_value = game.roll_to_x(roll_to)
        did_succeed.append(success)
        board_values.append(board_value)

    print("roll to: ", roll_to, " (", swords, "swords)")
    print("blue: ", blue_wheels, " orange: ", orange_wheels)
    print("success_rate: ", round(did_succeed.count(1) / rolls, 2))
    print("average value: ", sum(board_values) / rolls)
