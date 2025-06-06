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
    st.markdown("<h1 style='text-align: center;'>Cash Conversions</h1>", unsafe_allow_html=True)

    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    launch_2 = middle.button("£2", use_container_width=True)
    launch_5 = middle.button("£5", use_container_width=True)
    launch_25 = middle.button("£25", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

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
        st.session_state.input_key = str(uuid.uuid4())
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
        st.session_state.input_key = str(uuid.uuid4())

    
    st.markdown(f"<h1 style='text-align: center;'>Cash Conversions at £{st.session_state.conversion_multiplier}</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_number} at {st.session_state.conversion_multiplier}")

    with st.form("answer_form"):
        user_input = st.text_input("What is the correct answer?", key=st.session_state.input_key)
        submitted = st.form_submit_button("Check", type = "primary")

        if submitted:
            try:
                user_value = float(user_input)
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

    #Inline button generation and functionality
    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.session_state.clear()
        st.switch_page("pages/roulette_cash.py")

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