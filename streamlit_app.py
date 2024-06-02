import streamlit as st

from PortRoyal import Letter, Player, Board, DenyStrategy
from analysis import get_rolling_results

st.title('Port Royal - Helper')

tries = 10000
roll_to = st.number_input(label="roll to", min_value=1, max_value=7, value=7)
count_wheels = st.checkbox(label="count_wheels", value=True)

with st.expander("Player Details"):
    swords = st.number_input(label="swords", min_value=0, max_value=7, value=0)
    blue_wheels = st.number_input(label="blue wheels", min_value=0, max_value=3, value=0)
    orange_wheels = st.number_input(label="orange wheels", min_value=0, max_value=3, value=0)
    deny_strategy = st.selectbox(label="deny strategy", options=[DenyStrategy.NEVER, DenyStrategy.ALWAYS, DenyStrategy.SMART])

st.title('Board')
with st.expander("Ships"):
    yellow_ship = st.selectbox(label="yellow ship", options=[None, Letter.A, Letter.B, Letter.C])
    orange_ship = st.selectbox(label="orange ship", options=[None, Letter.A, Letter.B, Letter.C])
    green_ship = st.selectbox(label="green ship", options=[None, Letter.A, Letter.B, Letter.C])
    blue_ship = st.selectbox(label="blue ship", options=[None, Letter.A, Letter.B, Letter.C, Letter.D])
    red_ship = st.selectbox(label="red ship", options=[None, Letter.A, Letter.B, Letter.C, Letter.D])
    black_ship = st.selectbox(label="black ship", options=[None, Letter.A, Letter.B, Letter.C, Letter.D, Letter.E])
with st.expander("Wheels"):
    yellow_wheel = st.selectbox(label="yellow wheel", options=[None, Letter.D, Letter.E])
    orange_wheel = st.selectbox(label="orange wheel", options=[None, Letter.D, Letter.E])
    green_wheel = st.selectbox(label="green wheel", options=[None, Letter.D, Letter.E])
    blue_wheel = st.selectbox(label="blue wheel", options=[None, Letter.E])
    red_wheel = st.selectbox(label="red wheel", options=[None, Letter.E])

# Test it
player = Player(swords=swords, blue_wheels=blue_wheels, orange_wheels=orange_wheels, deny_strategy=deny_strategy)
board = Board(
    yellow_ship=yellow_ship,
    orange_ship=orange_ship,
    green_ship=green_ship,
    blue_ship=blue_ship,
    red_ship=red_ship,
    black_ship=black_ship,
    yellow_wheel=yellow_wheel,
    orange_wheel=orange_wheel,
    green_wheel=green_wheel,
    blue_wheel=blue_wheel,
    red_wheel=red_wheel
)
data_success = get_rolling_results(tries=tries, roll_to=roll_to, count_wheels=count_wheels, board=board, player=player)

success_rate = round((data_success.count(1) / tries) * 100, 2)
st.title("Success Rate:  " + str(success_rate) + "%")
