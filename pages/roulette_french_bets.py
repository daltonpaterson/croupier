import streamlit as st
import random
import uuid

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
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    launch_tier = middle.button("Tier", use_container_width=True)
    launch_orphelins = middle.button("Orphelins", use_container_width=True)
    launch_voisin = middle.button("Voisin", use_container_width=True)
    launch_mixed = middle.button("Mixed", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    if launch_tier:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 6
        st.session_state.mixed = False
        st.rerun()

    if launch_orphelins:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 5
        st.session_state.mixed = False
        st.rerun()

    if launch_voisin:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 9
        st.session_state.mixed = False
        st.rerun()

    if launch_mixed:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mixed = True
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")
else:
    # Question Pool - Default range set to Easy
    question_pool = DIFFICULTY_RANGES.get(st.session_state.difficulty, DIFFICULTY_RANGES["Easy"])

    def reset_question():
        question = generate_question()
        st.session_state.question_text = question[0]
        st.session_state.question_number = question[1]
        st.session_state.correct_answer = question[2]
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.input_key = str(uuid.uuid4())
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    def generate_question():
        if st.session_state.mixed == True:
            bets = [("Tier", 6), ("Orphelins", 5), ("Voisin", 9)]
            bet1, bet2 = random.sample(bets, 2)
            combined_pieces = bet1[1] + bet2[1]
            amount = random.choice(question_pool)

            
            return f"{bet1[0]} and {bet2[0]} by {amount}", amount, combined_pieces * amount
        else:
            if st.session_state.conversion_multiplier == 6:
                french_bet = "Tier"
            elif st.session_state.conversion_multiplier == 5:
                french_bet = "Orphelins"
            elif st.session_state.conversion_multiplier == 9:
                french_bet = "Voisin"

            amount = random.choice(question_pool)
            
            #Returns a tuple in the following format - Question text, amount to multiply, answer
            return f"{french_bet} by {amount}", {amount}, st.session_state.conversion_multiplier * amount

    # Initialize session state for game
    if "question_number" not in st.session_state:
        question = generate_question()
        st.session_state.question_text = question[0]
        st.session_state.question_number = question[1]
        st.session_state.correct_answer = question[2]
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = str(uuid.uuid4())

    st.title(f"French Bets")
    st.subheader(f"{st.session_state.question_text}")

    with st.form("answer_form"):
        user_input = st.text_input("What is the correct answer?", key=st.session_state.input_key)
        submitted = st.form_submit_button("Check", type = "primary")
        if submitted:
            try:
                user_value = int(user_input)
                correct_value = st.session_state.correct_answer
                is_correct = abs(user_value - correct_value) < 0.01

                if st.session_state.correct and is_correct:
                    reset_question()

                st.session_state.correct = is_correct
                st.session_state.show_result = True
                st.session_state.correct_answer = correct_value
            except ValueError:
                st.error("Please enter a valid number.")

    if st.session_state.show_result:
        if st.session_state.correct:
            st.success("✅ Correct! - Press enter to recieve a new question")
        elif st.session_state.show_answer:
            st.info(f"💡 The correct answer is {st.session_state.correct_answer}")
        else:
            st.error(f"❌ Incorrect. The correct answer was {st.session_state.correct_answer}")

    #Create inline buttons
    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.session_state.clear()
        st.switch_page("pages/roulette_french_bets.py")

    # Autofocus text input
    st.components.v1.html(f"""
        <script>
            setTimeout(function() {{
                const formInputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (formInputs.length > 0) {{
                    formInputs[formInputs.length - 1].focus();
                }}
            }}, 150);
        </script>
    """, height=0)