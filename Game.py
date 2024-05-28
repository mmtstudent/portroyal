from Helper import Board, TwoDice, roll_color, roll_letter


class Game:
    rerolled_letter: chr = None
    board: Board
    roll_to: int
    swords: int
    blue_wheels: int
    orange_wheels: int
    ships_on_board: int
    wheels_on_board: int

    def __init__(self,
                 roll_to: int,
                 game_swords: int,
                 game_blue_wheels: int,
                 game_orange_wheels: int,
                 ships_on_board: int = 0,
                 wheels_on_board: int = 0,
                 ):
        self.roll_to = roll_to
        self.swords = game_swords
        self.blue_wheels = game_blue_wheels
        self.orange_wheels = game_orange_wheels
        self.ship_on_board = ships_on_board
        self.wheels_on_board = wheels_on_board
        self.board = Board(board_ships={}, board_wheels={})
        while len(self.board.board_ships) < ships_on_board:
            self.board.board_ships[roll_color()] = 'a'
        while len(self.board.board_wheels) < wheels_on_board:
            color = roll_color()
            while color == 'black':
                color = roll_color()
            self.board.board_wheels[color] = 'e'

    def should_take(self, roll):
        take_ship = True
        # only deny if it is not the last ship you need and if you have more than 0 swords
        if len(self.board.board_ships) + len(self.board.board_wheels) < self.roll_to - 1 and self.swords > 0:
            match roll.color:
                # always deny black if you have 4+ swords?
                case 'black':
                    if self.swords >= 4:
                        if roll.swords <= self.swords:
                            take_ship = False
                case 'red' | 'blue':
                    if 'black' not in self.board.board_ships and self.swords >= 4:
                        take_ship = False
        return take_ship

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
            if roll.color not in self.board.board_ships:
                take_ship = self.should_take(roll)
                if take_ship:
                    board.board_ships[roll.color] = [roll.letter]
            else:
                if roll.swords > self.swords:
                    if self.orange_wheels > 0 and roll.swords < self.swords + 2:
                        # Deny and use orange wheel
                        self.orange_wheels -= 1
                    elif self.orange_wheels > 1 and roll.swords < self.swords + 4:
                        # Deny and use orange wheel
                        self.orange_wheels -= 2
                    elif self.blue_wheels > 0:
                        # Use Blue wheel to re-roll color
                        self.blue_wheels -= 1
                        self.rerolled_letter = roll.letter
                    else:
                        board.is_failed = True
        return board

    def roll_to_x_items(self, x: int):
        while len(self.board.board_ships) + len(self.board.board_wheels) < x:
            board = self.roll_dice(self.board)
            if board.is_failed:
                return 0, *self.sum_up_dice(self.board.take_dice)
        return 1, *self.sum_up_dice(self.board.take_dice)

    def roll_to_x_ships(self, x: int):
        if self.swords >= 4:
            return self.roll_to_x_items(5)
        if self.swords >= 5:
            return self.roll_to_x_items(6)
        while len(self.board.board_ships) < x and len(self.board.board_wheels) + len(self.board.board_ships) < 6:
            board = self.roll_dice(self.board)
            if board.is_failed:
                return 0, *self.sum_up_dice(self.board.take_dice)
        return 1, *self.sum_up_dice(self.board.take_dice)

    def start_game(self, roll_to_x: int, roll_to_end: bool):
        if roll_to_end:
            return self.roll_to_x_items(roll_to_x)
        else:
            return self.roll_to_x_ships(roll_to_x)

    def calculate_swords(self, movement):
        # +5 from diplomat before 5.
        # no treasures
        if movement > 39:
            self.swords = 5
        elif movement >= 30:
            self.swords = 4
        elif movement >= 12:
            self.swords = 2
        else:
            self.swords = 0

    def sum_up_dice(self, dice_list: list[TwoDice]):
        if len(dice_list) == 0:
            return 2, 1
        sum_movement = 0
        sum_skulls = 0
        for dice in dice_list:
            sum_movement += dice.movement
            sum_skulls += dice.skulls
            if dice.is_wheel and dice.color == 'orange':
                self.orange_wheels += 1
            if dice.is_wheel and dice.color == 'blue':
                self.blue_wheels += 1
        return sum_movement, sum_skulls
