from PortRoyal.roll import Roll
from PortRoyal.utils import Color, Letter


class Board:
    def __init__(self,
                 blue_ship: Letter | None = None,
                 orange_ship: Letter | None= None,
                 yellow_ship: Letter | None = None,
                 red_ship: Letter | None = None,
                 black_ship: Letter | None = None,
                 green_ship: Letter | None = None,
                 blue_wheel: Letter | None = None,
                 orange_wheel: Letter | None = None,
                 yellow_wheel: Letter | None = None,
                 red_wheel: Letter | None = None,
                 green_wheel: Letter | None = None):
        self.ships = {
            Color.BLUE: blue_ship,
            Color.ORANGE: orange_ship,
            Color.YELLOW: yellow_ship,
            Color.RED: red_ship,
            Color.BLACK: black_ship,
            Color.GREEN: green_ship,
        }
        self.wheels = {
            Color.BLUE: blue_wheel,
            Color.ORANGE: orange_wheel,
            Color.YELLOW: yellow_wheel,
            Color.RED: red_wheel,
            Color.GREEN: green_wheel,
        }

    @classmethod
    def from_board(cls, board: "Board"):
        return cls(
            blue_ship=board.ships.get(Color.BLUE),
            orange_ship=board.ships.get(Color.ORANGE),
            yellow_ship=board.ships.get(Color.YELLOW),
            red_ship=board.ships.get(Color.RED),
            black_ship=board.ships.get(Color.BLACK),
            green_ship=board.ships.get(Color.GREEN),
            blue_wheel=board.wheels.get(Color.BLUE),
            orange_wheel=board.wheels.get(Color.ORANGE),
            yellow_wheel=board.wheels.get(Color.YELLOW),
            red_wheel=board.wheels.get(Color.RED),
            green_wheel=board.wheels.get(Color.GREEN)
        )

    def count_items(self) -> int:
        return self.count_ships() + self.count_wheels()

    def count_ships(self) -> int:
        return sum(1 for ship in self.ships.values() if ship)

    def count_wheels(self) -> int:
        return sum(1 for wheel in self.wheels.values() if wheel)

    def add_roll(self, roll: Roll) -> None:
        if roll.is_wheel():
            self.wheels[roll.color] = roll.letter
        else:
            self.ships[roll.color] = roll.letter

