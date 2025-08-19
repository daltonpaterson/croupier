import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="Roulette Full Completes"
)

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 20, 5)),     # 5 to 15
    "Medium": list(range(20, 55, 5)),   # 20 to 50
    "Hard": list(range(55, 100, 5)),   # 55 to 100
}

COMPLETE_PIECES = {
    "'0'": [17,235],
    "'1 or 3'": [27, 297],
    "'2'": [36, 396],
    "'34 or 36'": [18, 198],
    "'35'": [24, 264],
    "'middle numbers'": [40, 392],
    "'outside numbers'": [30, 294],
}


# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.markdown("<h1 style='text-align: center;'>Full Completes</h1>", unsafe_allow_html=True)
    
    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )

    launch_pieces = middle.button("Pieces", use_container_width=True)
    launch_payouts = middle.button("Payouts", use_container_width=True)
    launch_bet_cost = middle.button("Cost", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    for mode, button in [
        ("Pieces", launch_pieces),
        ("Payouts", launch_payouts),
        ("Cost", launch_bet_cost)]:
        if button:
            st.session_state.difficulty = difficulty
            st.session_state.difficulty_chosen = True
            st.session_state.mode = mode
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
        st.session_state.input_key = int(uuid.uuid4())
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True
    
    def generate_complete_pieces_question():
        question = random.choice(list(COMPLETE_PIECES.keys()))
        answer = COMPLETE_PIECES[question]

        return f"Full complete piece count for {question}", answer[0], answer[0]

    def generate_complete_payout_question():
        question = random.choice(list(COMPLETE_PIECES.keys()))
        answer = COMPLETE_PIECES[question]

        return f"Full complete payout for {question}", answer[1], answer[1]
    
    def generate_complete_cost_question():
        question = random.choice(list(COMPLETE_PIECES.keys()))
        answer = COMPLETE_PIECES[question]
        amount = random.choice(question_pool)
        cost = answer[0] * amount
        
        return f"Cost to place a full complete on {question} by {amount}", cost, cost

    
    def generate_question():
        mode = st.session_state.mode
        if mode == "Pieces":
            return generate_complete_pieces_question()
        elif mode == "Payouts":
            return generate_complete_payout_question()
        elif mode == "Cost":
            return generate_complete_cost_question()

    # Initialize session state for game
    if "question_number" not in st.session_state:
        question = generate_question()
        st.session_state.question_text = question[0]
        st.session_state.question_number = question[1]
        st.session_state.correct_answer = question[2]
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())

    st.markdown("<h1 style='text-align: center;'>Full Completes</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_text}")

    with st.form("answer_form"):
        user_input = st.number_input("What is the correct answer?", placeholder= "Enter amount", value=None, format="%d", step=5, key=st.session_state.input_key)
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
        st.switch_page("pages/roulette_fullcomplete.py")

    # Autofocus text input
    st.components.v1.html(f"""
        <script>
            setTimeout(function() {{
                const formInputs = window.parent.document.querySelectorAll('input[type="number"]');
                if (formInputs.length > 0) {{
                    formInputs[formInputs.length - 1].focus();
                }}
            }}, 150);
        </script>
    """, height=0)