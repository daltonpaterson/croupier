import streamlit as st

left, middle, right = st.columns(3, vertical_alignment="center")

middle.divider()
payouts = middle.button("Payouts", use_container_width=True, disabled=True)
cash_conversions = middle.button("Cash Conversions", use_container_width=True)
straight_ups = middle.button("Straight Up Conversions", use_container_width=True, disabled=True)
middle.divider()
french_bets = middle.button("French Bets", use_container_width=True, disabled=True)
french_bets_cash = middle.button("French Bets - Cash", use_container_width=True, disabled=True)
neighbour_bets = middle.button("Neighbour Bets", use_container_width=True, disabled=True)
middle.divider()
return_to_menu = middle.button("Return to Main Menu", use_container_width=True)

if cash_conversions:
    st.switch_page("pages/roulette_cash.py")
if return_to_menu:
    st.switch_page("main.py")