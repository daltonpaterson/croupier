import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="Roulette Straight Ups"
)

DIFFICULTY_RANGES = {
    "Easy": list(range(20, 55, 5)),     # 5 to 50
    "Medium": list(range(20, 105, 5)),   # 5 to 100
    "Hard": list(range(20, 205, 5)),   # 5 to 200
}

# -------------------
# Difficulty selection
# -------------------

if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.markdown("<h1 style='text-align: center;'>Paying Straight Ups</h1>", unsafe_allow_html=True)

    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )

    straight_up = middle.button("Continue", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    if straight_up:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 35
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")
else:
    # --------------------
    # Conversion Logic
    # --------------------

    def reset_question():
        current = st.session_state.question_number
        available = [q for q in question_pool if q != current]
        st.session_state.question_number = random.choice(available)
        st.session_state.correct_answer = st.session_state.question_number * st.session_state.conversion_multiplier
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    # Question Pool - Default range set to Easy
    question_pool = DIFFICULTY_RANGES.get(st.session_state.difficulty, DIFFICULTY_RANGES["Easy"])

    # Initialize session state for game
    if "question_number" not in st.session_state:
        st.session_state.question_number = random.choice(question_pool)
        st.session_state.correct_answer = st.session_state.question_number * st.session_state.conversion_multiplier
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())

    st.markdown("<h1 style='text-align: center;'>Paying Straight Ups</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_number} on the number")

    with st.form("answer_form"):
        user_input = st.number_input("What is the correct answer?", placeholder= "Enter amount", value=None, format="%d", step=5, key=st.session_state.input_key)
        submitted = st.form_submit_button("Check", type = "primary")

        if submitted:
            try:
                user_value = int(user_input)
                correct_value = st.session_state.question_number * st.session_state.conversion_multiplier
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

    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.session_state.clear()
        st.switch_page("pages/roulette_straight_up.py")

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