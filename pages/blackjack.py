import streamlit as st
import random
import uuid

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 55, 5)),     # 5 to 50
    "Medium": list(range(50, 155, 5)),   # 5 to 150
    "Hard": list(range(150, 505, 5)),   # 10 to 500
    "Kyle": list(range(1, 21, 1)),    # 1 to 20
}

# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.title("Select Difficulty")
    difficulty = st.radio(
        "Choose your difficulty:",
        options=["Easy", "Medium", "Hard", "Kyle"],
    )
    if st.button("Start Game"):
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.rerun()
else:
    # --------------------
    # Blackjack game logic
    # --------------------


    def reset_question():
        current = st.session_state.question_number
        available = [q for q in question_pool if q != current]
        st.session_state.question_number = random.choice(available)
        st.session_state.correct_answer = st.session_state.question_number * 1.5
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
        st.session_state.correct_answer = st.session_state.question_number * 1.5
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = str(uuid.uuid4())


    st.title("🃏 Blackjack")
    st.write(f"Difficulty: **{st.session_state.difficulty}**")
    st.subheader(f"Blackjack on {st.session_state.question_number}")

    with st.form("answer_form"):
        user_input = st.number_input("What is the correct answer?", key=st.session_state.input_key, value=None)
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                user_value = float(user_input)
                correct_value = st.session_state.question_number * 1.5
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
            st.success("✅ Correct!")
        elif st.session_state.show_answer:
            st.info(f"💡 The correct answer is {st.session_state.correct_answer}")
        else:
            st.error(f"❌ Incorrect. The correct answer was {st.session_state.correct_answer}")


    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.switch_page("main.py")

    

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