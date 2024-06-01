import random
from enum import Enum


class Color(Enum):
    BLUE = "blue"
    ORANGE = "orange"
    YELLOW = "yellow"
    RED = "red"
    BLACK = "black"
    GREEN = "green"


class Ship(Enum):
    BLUE = Color.BLUE
    ORANGE = Color.ORANGE
    YELLOW = Color.YELLOW
    RED = Color.RED
    BLACK = Color.BLACK
    GREEN = Color.GREEN


class Wheel(Enum):
    BLUE = Color.BLUE
    ORANGE = Color.ORANGE
    YELLOW = Color.YELLOW
    RED = Color.RED
    GREEN = Color.GREEN


class Letter(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


def roll_color_dice() -> Color:
    return random.choice(list(Color))


def roll_letter_dice() -> Color:
    return random.choice(list(Letter) + [Letter.B])
