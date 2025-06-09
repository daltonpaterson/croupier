import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="Three Card Side Bets"
)

DIFFICULTY_RANGES = {
    "Easy": list(range(5, 20, 5)),     # 5 to 15
    "Medium": list(range(5, 55, 5)),   # 5 to 50
    "Hard": list(range(5, 105, 5)),   # 5 to 105
}

# -------------------
# Difficulty selection
# -------------------
if "difficulty_chosen" not in st.session_state:
    st.session_state.difficulty_chosen = False
    st.session_state.difficulty = None

if not st.session_state.difficulty_chosen:
    st.markdown("<h1 style='text-align: center;'>Three Card Poker Side Bets</h1>", unsafe_allow_html=True)
    
    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    colour_bonus = middle.selectbox(
        "Matching Colour Bonus:",
        options=["Enable", "Disable"],
        accept_new_options=False,
        index=1
    )
    launch_prime = middle.button("Prime", use_container_width=True)
    launch_colour = middle.button("Colour Bonus", use_container_width=True)
    launch_mixed = middle.button("Mixed", use_container_width=True)
    return_to_menu = middle.button("Return to Main Menu", use_container_width=True)

    if colour_bonus == "Enable":
        st.session_state.colour_bonus = True
    else:
        st.session_state.colour_bonus = False

    if launch_prime:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "Prime"
        st.rerun()

    if launch_colour:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "Colour"
        st.rerun()

    if launch_mixed:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.mode = "Mixed"
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("main.py")
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

    def generate_prime_question():

        bets = [("Pair", 1), ("Flush", 4), ("Straight", 6), ("Three of a Kind", 33), ("Straight Flush", 35)]

        question = random.choice(bets)
        amount = random.choice(question_pool)
        #Returns a tuple in the following format - Question text, amount to multiply, answer
        return f"{question[0]} at {amount}", amount, amount * question[1]
        
    
    def generate_colour_question():
        amount = random.choice(question_pool)
        if st.session_state.colour_bonus == True:
            return f"Colour Bonus at {amount} (Matching Colour)", amount, amount * 4
        else:
            return f"Colour Bonus at {amount}", amount, amount * 3

    def generate_question():
        mode = st.session_state.mode
        if mode == "Prime":
            return generate_prime_question()
        if mode == "Colour":
            return generate_colour_question()
        else:
            mixed_question = random.choice([generate_prime_question, generate_colour_question])
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
        st.switch_page("pages/threecard_sidebets.py")

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