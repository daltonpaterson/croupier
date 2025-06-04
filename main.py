import streamlit as st

# -----
# Main Menu Layout
# -----

left, middle, right = st.columns(3, vertical_alignment="center")

middle.divider()
roulette = middle.button("Roulette", use_container_width=True)
blackjack = middle.button("Blackjack", use_container_width=True)
middle.divider()

# -----
# Navigation Functionality
# -----

if roulette:
    st.switch_page("pages/roulette_menu.py")
if blackjack:
    st.switch_page("pages/blackjack_menu.py")