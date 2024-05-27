import streamlit as st
from Game import Game

st.title('Port Royal - Helper')

rolls = 100000
roll_to = st.number_input(label="roll to", min_value=1, max_value=7, value=7)
swords = st.number_input(label="swords", min_value=0, max_value=7, value=0)
blue_wheels = st.number_input(label="blue wheels", min_value=0, max_value=3, value=0)
orange_wheels = st.number_input(label="orange wheels", min_value=0, max_value=3, value=0)


def play_round(rolls, roll_to, swords, blue_wheels, orange_wheels):
    did_succeed = []
    board_values = []
    for i in range(0, rolls):
        game = Game(game_swords=swords, game_blue_wheels=blue_wheels, game_orange_wheels=orange_wheels)
        # success, board_value = game.roll_to_min_x(roll_to)
        success, board_value = game.roll_to_x(roll_to)
        did_succeed.append(success)
        board_values.append(board_value)
    return did_succeed, board_values


data_success, data_values = play_round(rolls, roll_to, swords, blue_wheels, orange_wheels)

success_rate = round(data_success.count(1) / rolls, 2)
st.title("success_rate:")
st.title(success_rate)
