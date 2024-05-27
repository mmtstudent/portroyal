from Game import Game

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
