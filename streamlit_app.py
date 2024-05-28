import streamlit as st

from main import play_games

st.title('Port Royal - Helper')

rolls = 100000
roll_to = st.number_input(label="roll to", min_value=1, max_value=7, value=7)
roll_to_end = st.checkbox(label="count_wheels", value=True)
swords = st.number_input(label="swords", min_value=0, max_value=7, value=0)
blue_wheels = st.number_input(label="blue wheels", min_value=0, max_value=3, value=0)
orange_wheels = st.number_input(label="orange wheels", min_value=0, max_value=3, value=0)

current_ships = st.number_input(label="current ships", min_value=0, max_value=5, value=0)
current_wheels = st.number_input(label="current wheels", min_value=0, max_value=5, value=0)


data_success, movement_list, skulls_list = play_games(rolls, roll_to, swords, blue_wheels, orange_wheels, current_ships,
                                                      current_wheels, roll_to_end)

success_rate = round(data_success.count(1) / rolls, 2)
st.title("success_rate:")
st.title(success_rate)

avg_value = round(sum(movement_list) / rolls, 2)
st.title("avg_movement:")
st.title(avg_value)

avg_skulls = round(sum(skulls_list) / rolls, 2)
st.title("avg_skulls:")
st.title(avg_skulls)
