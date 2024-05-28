from Game import Game


def play_games(rolls, roll_to, swords, blue_wheels, orange_wheels, current_ships, current_wheels, roll_to_end):
    did_succeed = []
    movement_list = []
    skulls_list = []
    for i in range(0, rolls):
        game = Game(game_swords=swords, game_blue_wheels=blue_wheels, game_orange_wheels=orange_wheels,
                    ships_on_board=current_ships, wheels_on_board=current_wheels, roll_to=roll_to)
        success, movement, skulls = game.start_game(roll_to, roll_to_end)
        did_succeed.append(success)
        movement_list.append(movement)
        skulls_list.append(skulls)
    return did_succeed, movement_list, skulls_list


if __name__ == '__main__':
    rolls = 100000
    roll_to = 3
    swords = 0
    blue_wheels = 0
    orange_wheels = 0
    current_ships = 0
    current_wheels = 0
    roll_to_end = True

    data_success, movement_list, skulls_list = play_games(rolls, roll_to, swords, blue_wheels, orange_wheels,
                                                          current_ships, current_wheels, roll_to_end)

    print("roll to: ", roll_to, " (", swords, "swords)")
    print("blue: ", blue_wheels, " orange: ", orange_wheels)
    print("success_rate: ", round(data_success.count(1) / rolls, 2))
    print("average value: ", sum(movement_list) / rolls)
