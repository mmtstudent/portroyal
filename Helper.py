from dataclasses import dataclass, field

import random


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
    def movement(self) -> float:
        if self.is_wheel:
            match self.color:
                case 'yellow' | 'red':
                    return 3
                case 'green':
                    return 3
                case 'orange':
                    return 0
                case 'blue':
                    return 0

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
    def value(self) -> float:
        if self.is_wheel:
            # todo - how much is a wheel worth?
            match self.color:
                case 'yellow' | 'red' | 'orange':
                    return 1.8
                case 'blue' | 'green':
                    return 2.1
        else:
            return self.movement - self.skulls * 1.1

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


@dataclass
class Board:
    board_ships: {}
    board_wheels: {}
    is_failed: bool = False

    @property
    def take_dice(self) -> list[TwoDice]:
        value_list = []
        if self.is_failed:
            return value_list
        for item in self.board_ships:
            value_list.append(TwoDice(item, self.board_ships[item][0]))
        for item in self.board_wheels:
            value_list.append(TwoDice(item, self.board_wheels[item][0]))
        value_list.sort(key=lambda x: x.value, reverse=True)
        take_x = max(len(value_list) - 3, 1)
        self.board_ships = {}
        self.board_wheels: {}
        return value_list[-take_x:]
