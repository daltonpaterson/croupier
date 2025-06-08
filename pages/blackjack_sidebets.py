import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="Blackjack Side Bets"
)

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 20, 5)),     # 5 to 15
    "Medium": list(range(5, 35, 5)),   # 5 to 30
    "Hard": list(range(5, 55, 5)),   # 5 to 55
}

# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.markdown("<h1 style='text-align: center;'>Blackjack Side Bets</h1>", unsafe_allow_html=True)
    
    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    trip_bonus = middle.selectbox(
        "Trips Bonus:",
        options=["Enable", "Disable"],
        accept_new_options=False,
        index=1
    )
    launch_pairs = middle.button("Pairs", use_container_width=True)
    launch_213 = middle.button("21+3", use_container_width=True)
    launch_mixed = middle.button("Mixed", use_container_width=True)
    return_to_menu = middle.button("Return to Blackjack Menu", use_container_width=True)

    if trip_bonus == "Enable":
        st.session_state.trips_bonus = True
    else:
        st.session_state.trips_bonus = False

    if launch_pairs:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "Pairs"
        st.rerun()

    if launch_213:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "213"
        st.rerun()

    if launch_mixed:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "Mixed"
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/blackjack_menu.py")
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

    def generate_pair_question():
        if st.session_state.trips_bonus == True:
            bets = [("Mixed Pair", 10), ("Coloured Pair", 15), ("Perfect Pair", 35)]
        else:
            bets = [("Mixed Pair", 5), ("Coloured Pair", 10), ("Perfect Pair", 30)]

        question = random.choice(bets)
        amount = random.choice(question_pool)
        #Returns a tuple in the following format - Question text, amount to multiply, answer

        if st.session_state.trips_bonus == True:
            return f"{question[0]} at {amount} (Trips Bonus)", amount, amount * question[1]
        else:
            return f"{question[0]} at {amount}", amount, amount * question[1]
        
    
    def generate_213_question():
        amount = random.choice(question_pool)
        return f"21+3 at {amount}", amount, amount * 9

    def generate_question():
        mode = st.session_state.mode
        if mode == "Pairs":
            return generate_pair_question()
        if mode == "213":
            return generate_213_question()
        else:
            mixed_question = random.choice([generate_pair_question, generate_213_question])
            return mixed_question()


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

    st.markdown("<h1 style='text-align: center;'>Blackjack Side Bets</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_text}")

    with st.form("answer_form"):
        #user_input = st.text_input("How much does the bet pay?", key=st.session_state.input_key)
        user_input = st.number_input("How much does the bet pay?", value=None ,placeholder="Enter cash amount", format="%d", step=5, key=st.session_state.input_key)
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
        st.switch_page("pages/blackjack_sidebets.py")

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