import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="House Edges"
)

# -------------------
# Difficulty selection
# -------------------
if "mode_chosen" not in st.session_state:
    st.session_state.mode_chosen = False

if not st.session_state.mode_chosen:
    st.markdown("<h1 style='text-align: center;'>House Edge</h1>", unsafe_allow_html=True)
    
    left, middle, right = st.columns(3, vertical_alignment="center")
    
    blackjack_decks = middle.selectbox(
        "Blackjack Decks:",
        options=["Four Decks", "Six Decks"],
        accept_new_options=False,
        index=1
    )

    launch_roulette = middle.button("Roulette", use_container_width=True)
    launch_blackjack = middle.button("Blackjack", use_container_width=True)
    launch_threecard = middle.button("Three Card Poker", use_container_width=True)
    launch_uth = middle.button("Ultimate Texas Hold'em", use_container_width=True)
    launch_punto = middle.button("Punto Banco", use_container_width=True, disabled=True)
    launch_mixed = middle.button("Mixed", use_container_width=True)
    return_to_menu = middle.button("Return to Main Menu", use_container_width=True)

    if blackjack_decks == "Six Decks":
        st.session_state.six_decks = True
    else:
        st.session_state.six_decks = False

    for mode, button in [
        ("Roulette", launch_roulette), 
        ("Blackjack", launch_blackjack),
        ("Three Card Poker", launch_threecard),
        ("Ultimate Texas Hold'em", launch_uth),
        ("Punto Banco", launch_punto),
        ("Mixed", launch_mixed)]:
        if button:
            st.session_state.mode_chosen = True
            st.session_state.mode = mode
            st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("main.py")
else:

    def reset_question():
        question = generate_question()
        st.session_state.question_text = question[0]
        st.session_state.correct_answer = question[1]
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    def generate_roulette_question():
        questions = [
            ("a Single Zero Wheel Number", 2.7),
            ("a Single Zero Wheel Even Chance", 1.35),
            ("a Double Zero Wheel Number", 5.26),
            ("a Double Zero Wheel Even Chance", 2.63)]

        question = random.choice(questions)
        #Returns a tuple in the following format - Question text, answer
        return f"What is the house edge of {question[0]}?", question[1]
    
    def generate_blackjack_question():
        if st.session_state.six_decks == True:
            questions = [
                ("[Six Deck] Blackjack (Best technique)", 0.55),
                ("[Six Deck] Blackjack (Best technique & draws soft 17)", 0.89),
                ("Ace King Suited", 19.17),
                ("[Six Deck] Bonus Pairs", 3.16),
                ("[Six Deck] 21+3", 3.23),
                ("[Six Deck] Top 3", 11.07)]
        else:
            questions =[
                ("[Four Deck] Blackjack (Best technique)", 0.51),
                ("[Four Deck] Blackjack (Best technique & draws soft 17)", 0.85),
                ("Ace King Suited", 19.17),
                ("[Four Deck] Bonus Pairs", 4.3),
                ("[Four Deck] 21+3", 4.24),
                ("[Four Deck] Top 3", 15.03)]

        question = random.choice(questions)
        #Returns a tuple in the following format - Question text, answer
        return f"What is the house edge of {question[0]}?", question[1]
    
    def generate_threecard_question():
        questions = [
            ("Three Card Poker - Ante", 2),
            ("Three Card Poker - Pair Plus", 2.7),
            ("Three Card Poker - Prime", 3.62)]

        question = random.choice(questions)
        #Returns a tuple in the following format - Question text, answer
        return f"What is the house edge of {question[0]}?", question[1]
    
    def generate_uth_question():
        questions = [
            ("Ultimate Texas Hold'em - Main Game", 1.15),
            ("Ultimate Texas Hold'em - Trips Bonus", 3.5)]

        question = random.choice(questions)
        #Returns a tuple in the following format - Question text, answer
        return f"What is the house edge of {question[0]}?", question[1]

    def generate_question():
        mode = st.session_state.mode
        if mode == "Roulette":
            return generate_roulette_question()
        elif mode == "Blackjack":
            return generate_blackjack_question()
        elif mode == "Three Card Poker":
            return generate_threecard_question()
        elif mode == "Ultimate Texas Hold'em":
            return generate_uth_question()
        else:
            mixed_question = random.choice(
                [generate_roulette_question, 
                 generate_blackjack_question,
                 generate_threecard_question,
                 generate_uth_question
                 ])
            return mixed_question()


    # Initialize session state for game
    if "question_text" not in st.session_state:
        question = generate_question()
        st.session_state.question_text = question[0]
        st.session_state.correct_answer = question[1]
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key = int(uuid.uuid4())

    st.markdown("<h1 style='text-align: center;'>House Edges</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_text}")

    with st.form("answer_form"):
        user_input = st.number_input("What is the house edge percentage?", value=None ,placeholder="", format="%.2f", step=1.0, key=st.session_state.input_key)
        submitted = st.form_submit_button("Check", type = "primary")
        if submitted:
            try:
                user_value = float(user_input)
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
        st.switch_page("pages/houseedge.py")

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