import streamlit as st

st.set_page_config(
    page_title="Croupier Training App",
    layout="centered",
)

# -----
# Main Menu Layout
# -----
st.markdown("<h1 style='text-align: center;'>Croupier Training App</h1>", unsafe_allow_html=True)
left, middle, right = st.columns(3, vertical_alignment="center")

middle.divider()
roulette = middle.button("Roulette", use_container_width=True)
blackjack = middle.button("Blackjack", use_container_width=True)
three_card_poker = middle.button("Three Card Poker", use_container_width=True)
ultimate_texas_poker = middle.button("Ultimate Texas Hold'em", use_container_width=True, disabled=True)
baccarat = middle.button("Baccarat", use_container_width=True, disabled=True)
middle.divider()

# -----
# Navigation Functionality
# -----

if roulette:
    st.switch_page("pages/roulette_menu.py")
if blackjack:
    st.switch_page("pages/blackjack_menu.py")
if three_card_poker:
    st.switch_page("pages/threecard_sidebets.py")