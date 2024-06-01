from copy import deepcopy

from PortRoyal import Letter
from PortRoyal.board import Board
from PortRoyal.game import Game
from PortRoyal.player import Player


def get_rolling_results(tries: int, roll_to: int, count_wheels: bool, player: Player, board: Board):
    did_succeed = []

    for i in range(0, tries):
        new_board = Board.from_board(board)
        new_player = deepcopy(player)
        game = Game(board=new_board, player=new_player)
        success = game.roll_to_x(roll_to=roll_to, count_wheels=count_wheels)
        did_succeed.append(success)
    return did_succeed


if __name__ == '__main__':
    tries = 1000
    roll_to = 7
    count_wheels = True

    #yellow_wheel = Letter.E
    # = Letter.E
    #red_wheel = Letter.E

    player = Player(swords=5)
    board = Board()

    data_success = get_rolling_results(
        tries=tries,
        roll_to=roll_to,
        count_wheels=count_wheels,
        player=player,
        board=board

    )

    print("roll to: ", roll_to, " (", player.swords, "swords)")
    print("blue: ", player.blue_wheels, " orange: ", player.orange_wheels)
    print("success_rate: ", round(sum(data_success) / tries, 2))
