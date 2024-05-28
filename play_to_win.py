
from Game import Game


def play_until_win(roll_to=3, swords=0, blue_wheels=0, orange_wheels=0, current_ships=0, current_wheels=0,
                   roll_to_end=False):
    game = Game(game_swords=swords, game_blue_wheels=blue_wheels, game_orange_wheels=orange_wheels,
                ships_on_board=current_ships, wheels_on_board=current_wheels, roll_to=roll_to)
    used_movement = 0
    used_skulls = 0
    rounds_to_end = 0
    while used_movement < (36 + 3 * max(0, used_skulls-8)):
        _, movement, skulls = game.start_game(roll_to, roll_to_end)
        used_movement += movement + 5
        used_skulls += skulls
        game.calculate_swords(used_movement)
        rounds_to_end += 1

    return rounds_to_end


if __name__ == '__main__':
    games = 10
    rounds_list = []
    for i in range(0, games):
        rounds = play_until_win()
        rounds_list.append(rounds)
    avg_rounds = sum(rounds_list)/games
    print(avg_rounds)
