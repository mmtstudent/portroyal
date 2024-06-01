from PortRoyal.utils import Letter, Color, roll_color_dice, roll_letter_dice


def roll_dice(letter: Letter = None, color: Color = None) -> "Roll":
    return Roll(letter=letter, color=color)


class Roll:
    def __init__(self, letter: Letter = None, color: Color = None):
        self.color = color if color else roll_color_dice()
        self.letter = letter if letter else roll_letter_dice()

    def get_swords(self) -> int:
        sum_swords = 0
        match self.letter:
            case Letter.A:
                sum_swords += 1
            case Letter.B:
                sum_swords += 2
            case Letter.C:
                sum_swords += 3
            case Letter.D:
                sum_swords += 4
            case Letter.E:
                sum_swords += 5

        match self.color:
            case Color.BLACK:
                sum_swords += 3
            case Color.RED | Color.BLUE:
                sum_swords += 2
            case Color.GREEN | Color.ORANGE:
                sum_swords += 1
            case Color.YELLOW:
                sum_swords += 0

        return sum_swords

    def is_wheel(self) -> bool:
        return (
                (self.color in (Color.GREEN, Color.ORANGE, Color.YELLOW) and self.letter in [Letter.D, Letter.E])
                or ((self.color in (Color.RED, Color.BLUE)) and self.letter in [Letter.E])
        )

    def get_movement(self) -> float:
        if self.is_wheel:
            match self.color:
                case Color.YELLOW | Color.RED:
                    return 3
                case Color.GREEN:
                    return 3
                case Color.ORANGE:
                    return 0
                case Color.BLUE:
                    return 0

        else:
            match self.letter:
                case Letter.A:
                    return 1
                case Letter.B:
                    return 2
                case Letter.C | Letter.D:
                    return 3
                case Letter.E:
                    return 4

    def get_skulls(self):
        if self.is_wheel:
            return 0
        else:
            match self.color, self.letter:
                case (Color.BLACK | Color.RED | Color.BLUE, Letter.C):
                    return 1
                case (Color.BLACK, Letter.E):
                    return 2
                case _:
                    return 0
