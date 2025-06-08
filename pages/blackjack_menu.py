import streamlit as st

st.set_page_config(
    page_title="Blackjack Menu"
)

st.markdown("<h1 style='text-align: center;'>Blackjack Menu</h1>", unsafe_allow_html=True)
left, middle, right = st.columns(3, vertical_alignment="center")
middle.divider()
blackjack = middle.button("Blackjack Payouts", use_container_width=True)
side_bets = middle.button("Side Bet Payouts", use_container_width=True)
middle.divider()
return_to_menu = middle.button("Return to Main Menu", use_container_width=True)

if blackjack:
    st.switch_page("pages/blackjack.py")
if side_bets:
    st.switch_page("pages/blackjack_sidebets.py")
if return_to_menu:
    st.switch_page("main.py")