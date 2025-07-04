import streamlit as st
import random
import uuid
from pages.tts import tts_question, tts_queue, tts_thread


st.set_page_config(
    page_title="Roulette French Bets"
)

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
    st.markdown("<h1 style='text-align: center;'>French Bets</h1>", unsafe_allow_html=True)
    
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
    launch_random = middle.button("Random", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    for mode, button in [
        ("Tier", launch_tier), 
        ("Orphelins", launch_orphelins),
        ("Voisin", launch_voisin),
        ("Mixed", launch_mixed),
        ("Random", launch_random)]:
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
        tts_question(question[0])
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    def generate_mixed_question():
        bets = [("Tier", 6), ("Orphelins", 5), ("Voisin", 9)]
        bet1, bet2 = random.sample(bets, 2)
        combined_pieces = bet1[1] + bet2[1]
        amount = random.choice(question_pool)

        return f"{bet1[0]} and {bet2[0]} by {amount}", amount, combined_pieces * amount

    def generate_french_question():
        mode = st.session_state.mode

        if mode == "Random":
            mode = random.choice(["Tier", "Orphelins", "Voisin"])

        if mode == "Tier":
            multiplier = 6
        elif mode == "Orphelins":
            multiplier = 5
        elif mode == "Voisin":
            multiplier = 9
            
        amount = random.choice(question_pool)
        
        #Returns a tuple in the following format - Question text, amount to multiply, answer
        return f"{mode} by {amount}", {amount}, multiplier * amount
    
    def generate_question():
        mode = st.session_state.mode
        if mode == "Mixed":
            return generate_mixed_question()
        elif mode == "Random":
            mixed_question = random.choice([generate_french_question, generate_mixed_question])
            return mixed_question()
        else:
            return generate_french_question()

    # Initialize session state for game
    if "question_number" not in st.session_state:
        question = generate_question()
        st.session_state.question_text = question[0]
        tts_question(question[0])
        st.session_state.question_number = question[1]
        st.session_state.correct_answer = question[2]
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())

    st.markdown("<h1 style='text-align: center;'>French Bets</h1>", unsafe_allow_html=True)
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
            tts_question("Correct")
        elif st.session_state.show_answer:
            st.info(f"💡 The correct answer is {st.session_state.correct_answer}")

        else:
            st.error(f"❌ Incorrect. The correct answer was {st.session_state.correct_answer}")
            tts_question("Incorrect)")

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
                const formInputs = window.parent.document.querySelectorAll('input[type="number"]');
                if (formInputs.length > 0) {{
                    formInputs[formInputs.length - 1].focus();
                }}
            }}, 150);
        </script>
    """, height=0)