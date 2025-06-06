import streamlit as st
import random
#import uuid

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 55, 5)),     # 5 to 50
    "Medium": list(range(50, 105, 5)),   # 50 to 100
    "Hard": list(range(100, 205, 5)),   # 100 to 200
}

# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.title("French Bets")
    left, middle, right = st.columns(3, vertical_alignment="center")
    
    max_cash = middle.number_input("Maximium Cash:", min_value= 50,placeholder="Enter cash amount", format="%d", step=25)
    launch_tier = middle.button("Tier", use_container_width=True)
    launch_orphelins = middle.button("Orphelins", use_container_width=True)
    launch_voisin = middle.button("Voisin", use_container_width=True)
    launch_all = middle.button("Mixed", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    if launch_tier:
            st.session_state.difficulty = int(max_cash)
            st.session_state.difficulty_chosen = True
            st.session_state.conversion_multiplier = 6
            st.rerun()
            st.error("Please enter a valid number.")


    if launch_orphelins:
        st.session_state.difficulty = int(max_cash)
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 5
        st.rerun()

    if launch_voisin:
        st.session_state.difficulty = int(max_cash)
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 9
        st.rerun()

    if launch_all:
        st.session_state.difficulty = int(max_cash)
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = "All"
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")
else:
    def reset_question():
        question = generate_question(st.session_state.difficulty, st.session_state.conversion_multiplier)
        st.session_state.question_text = question[0]
        st.session_state.correct_answer = question[1], question[2]
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.reset_inputs = True

        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    def generate_question(cash, multiplier):
        if multiplier == 6:
            new_cash = generate_french_cash(cash, multiplier)
            french_bet = "Tier"
            amount = (new_cash // 30) * 5
            change = new_cash % 30
        elif st.session_state.conversion_multiplier == 5:
            new_cash = generate_french_cash(cash, multiplier)
            french_bet = "Orphelins"
            amount = (new_cash // 25) * 5
            change = new_cash % 25
        elif st.session_state.conversion_multiplier == 9:
            new_cash = generate_french_cash(cash, multiplier)
            french_bet = "Voisin"
            amount = (new_cash // 45) * 5
            change = new_cash % 45

        elif multiplier == "All":
            french_bets = [25, 30, 45]
            multipliers = random.choice(french_bets)
            if multipliers == 30:
                new_cash = generate_french_cash(cash, 6)
                french_bet = "Tier"
                amount = (new_cash // 30) * 5
                change = new_cash % 30
            elif multipliers == 25:
                new_cash = generate_french_cash(cash, 5)
                french_bet = "Orphelins"
                amount = (new_cash // 25) * 5
                change = new_cash % 25
            elif multipliers == 45:
                new_cash = generate_french_cash(cash, 9)
                french_bet = "Voisin"
                amount = (new_cash // 45) * 5
                change = new_cash % 45

        #Question text, amount it goes by, change required
        return f"{french_bet} to the max - £{new_cash}", amount, change
    
    def generate_french_cash(cash, multiplier):
        try:
            cash = float(cash)
            multiplier = float(multiplier)
            start = int(multiplier * 5)
            end = int(cash) + 1

            if start >= end:
                st.warning("Multiplier too high for available cash. Adjusting to minimum valid value.")
                return start

            valid_cash_values = list(range(start, end, 25))
            return random.choice(valid_cash_values)

        except (ValueError, TypeError) as e:
            st.error(f"Invalid input for cash or multiplier: {e}")
            return 0


    # Initialize session state for game
    if "question_text" not in st.session_state:
        question = generate_question(st.session_state.difficulty, st.session_state.conversion_multiplier)
        st.session_state.question_text = question[0]
        st.session_state.correct_answer = question[1], question[2]
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
    
    if st.session_state.get("reset_inputs"):
        st.session_state["user_input_amount"] = " "
        st.session_state["user_input_change"] = " "
        st.session_state.reset_inputs = False  # Unset the flag

    st.title(f"French Bets - Cash")
    st.subheader(f"{st.session_state.question_text}")

    with st.form("answer_form"):
        user_input_amount = st.text_input("How much does it go by?", key="user_input_amount")
        user_input_cash = st.text_input("How much change should be given?", key="user_input_change")
        submitted = st.form_submit_button("Check", type = "primary")
        if submitted:
            try:
                
                if user_input_cash == "" or user_input_cash == " ":
                    change = int(0)
                else:
                    change = int(user_input_cash)

                user_value = int(user_input_amount), change
                correct_value = st.session_state.correct_answer
                is_correct = user_value == correct_value

                if st.session_state.correct and is_correct:
                    reset_question()

                st.session_state.correct = is_correct
                st.session_state.show_result = True
                st.session_state.correct_answer = correct_value
            except ValueError:
                st.error("Please enter a valid number.")

    if st.session_state.show_result:
        if st.session_state.correct:
            st.success("✅ Correct! - Press enter to receive a new question")
            st.session_state.show_answer = True
        elif st.session_state.show_answer:
            st.info(f"💡 The correct answer is goes by {st.session_state.correct_answer[0]} with £{st.session_state.correct_answer[1]} change")
        else:
            st.error(f"❌ Incorrect. The correct answer was goes by {st.session_state.correct_answer[0]} with £{st.session_state.correct_answer[1]} change")

    #Create inline buttons
    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.session_state.clear()
        st.switch_page("pages/roulette_french_bets_cash.py")