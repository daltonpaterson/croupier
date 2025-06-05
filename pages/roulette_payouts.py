import streamlit as st
import random
import uuid

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 101, 1)),     # 5 to 100
    "Medium": list(range(5, 301, 1)),   # 5 to 300
    "Hard": list(range(5, 501, 1)),   # 5 to 500
}

# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.title("Roulette Payouts")
    difficulty = st.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    change_required = st.selectbox(
        "Change Required:",
        options=["Enable", "Disable"],
        accept_new_options=False
    )

    left, middle, right = st.columns(3, vertical_alignment="center")
    launch_1 = middle.button("£1", use_container_width=True)
    launch_2 = middle.button("£2", use_container_width=True)
    launch_5 = middle.button("£5", use_container_width=True)
    launch_25 = middle.button("£25", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    if launch_1:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 1
        st.rerun()

    if launch_2:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 2
        st.rerun()

    if launch_5:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 5
        st.rerun()

    if launch_25:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 25
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")