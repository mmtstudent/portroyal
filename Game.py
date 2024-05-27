from Helper import Board, TwoDice, roll_color, roll_letter


class Game:
    rerolled_letter: chr = None
    board: Board

    def __init__(self,
                 game_swords: int,
                 game_blue_wheels: int,
                 game_orange_wheels: int,
                 ships_on_board: int = 0,
                 wheels_on_board: int = 0,
                 ):
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
                    elif self.orange_wheels > 0 and roll.swords < self.swords + 4:
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
        while len(self.board.board_ships) + len(self.board.board_wheels) < x:
            board = self.roll_dice(self.board)
            if board.is_failed:
                return 0, board.value
        return 1, self.board.value
