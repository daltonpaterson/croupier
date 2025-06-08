import streamlit as st
import random
import uuid

st.set_page_config(
    page_title="Roulette Payouts"
)

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
    st.markdown("<h1 style='text-align: center;'>Roulette Payouts</h1>", unsafe_allow_html=True)
    left, middle, right = st.columns(3, vertical_alignment="center")
    difficulty = middle.selectbox(
        "Select Difficulty:",
        options=["Easy", "Medium", "Hard"],
        accept_new_options=False
    )
    change_needed = middle.selectbox(
        "Change Required:",
        options=["Enable", "Disable"],
        accept_new_options=False,
        index=1
    )
    launch_1 = middle.button("£1", use_container_width=True)
    launch_2 = middle.button("£2", use_container_width=True)
    launch_5 = middle.button("£5", use_container_width=True)
    launch_25 = middle.button("£25", use_container_width=True)
    return_to_menu = middle.button("Return to Roulette Menu", use_container_width=True)

    if launch_1:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 1
        st.session_state.change_enabled = (change_needed == "Enable")
        st.rerun()

    if launch_2:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 2
        st.session_state.change_enabled = (change_needed == "Enable")
        st.rerun()

    if launch_5:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 5
        st.session_state.change_enabled = (change_needed == "Enable")
        st.rerun()

    if launch_25:
        st.session_state.difficulty = difficulty
        st.session_state.difficulty_chosen = True
        st.session_state.conversion_multiplier = 25
        st.session_state.change_enabled = (change_needed == "Enable")
        st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")
else:
    # --------------------
    # Payout Logic
    # --------------------

    # Question Pool - Default range set to Easy
    question_pool = DIFFICULTY_RANGES.get(st.session_state.difficulty, DIFFICULTY_RANGES["Easy"])
    
    def change_required():
        if st.session_state.conversion_multiplier == 2:
            return random.randrange(10, (st.session_state.correct_answer) + 1, 10)
        else:
            return random.randrange(25, (st.session_state.correct_answer) + 1, 25)

    def safe_int(value):
        if value == None:
            return 0
        else:
            return int(value)

    def reset_question():
        current = st.session_state.question_number
        available = [q for q in question_pool if q != current]
        st.session_state.question_number = random.choice(available)
        st.session_state.correct_answer = st.session_state.question_number * st.session_state.conversion_multiplier
        st.session_state.required_cash_change = change_required() if st.session_state.change_enabled else None
        st.session_state.correct = False
        st.session_state.show_result = False
        st.session_state.show_answer = False
        st.session_state.input_key = str(uuid.uuid4())
        st.session_state.reset_inputs = True
        st.rerun()
    
    def reveal_question():
        st.session_state.show_answer = True
        st.session_state.show_result = True

    # Initialize session state for game
    if "question_number" not in st.session_state:
        st.session_state.question_number = random.choice(question_pool)
        st.session_state.correct_answer = st.session_state.question_number * st.session_state.conversion_multiplier
        st.session_state.required_cash_change = change_required() if st.session_state.change_enabled else None
        st.session_state.show_result = False
        st.session_state.correct = False
        st.session_state.show_answer = False
        st.session_state.input_key_1 = int(uuid.uuid4())
        st.session_state.input_key_5 = int(uuid.uuid4())
        st.session_state.input_key_25 = int(uuid.uuid4())
        st.session_state.input_key_100 = int(uuid.uuid4())
        st.session_state.input_key_1000 = int(uuid.uuid4())


    if st.session_state.get("reset_inputs"):
        st.session_state.input_key_1 = int(uuid.uuid4())
        st.session_state.input_key_5 = int(uuid.uuid4())
        st.session_state.input_key_25 = int(uuid.uuid4())
        st.session_state.input_key_100 = int(uuid.uuid4())
        st.session_state.input_key_1000 = int(uuid.uuid4())
        st.session_state.reset_inputs = False  # Unset the flag

    st.markdown(f"<h1 style='text-align: center;'>Payout Simulator at £{st.session_state.conversion_multiplier}</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_number} at {st.session_state.conversion_multiplier}")

    if st.session_state.change_enabled:
        st.write(f"Give exactly £{st.session_state.required_cash_change} in cash.")

    with st.form("answer_form"):
        first_col, seond_col, third_col, fourth_col = st.columns(4, vertical_alignment="center")

        with first_col:
            grey_chip = st.image("assets/images/GreyChip.png")
            one_entry = st.number_input("1", value=None, min_value=0, format="%d", step=5, key=st.session_state.input_key_1, label_visibility="collapsed")
        with seond_col:
            red_chip = st.image("assets/images/RedChip.png")
            five_entry = st.number_input("1", value=None, min_value=0,format="%d", step=5, key=st.session_state.input_key_5, label_visibility="collapsed")
        with third_col:
            black_chip = st.image("assets/images/BlackChip.png")
            twenty_five_entry = st.number_input("1", value=None, min_value=0,format="%d", step=5, key=st.session_state.input_key_25, label_visibility="collapsed")
        with fourth_col:
            pink_chip = st.image("assets/images/PinkChip.png")
            one_hundred_entry = st.number_input("1", value=None, min_value=0,format="%d", step=5, key=st.session_state.input_key_100, label_visibility="collapsed")

        submitted = st.form_submit_button("Check", type = "primary")

        if submitted:
            if st.session_state.correct:
                reset_question()
            ones = safe_int(one_entry)
            fives = safe_int(five_entry)
            twenty_fives = safe_int(twenty_five_entry)
            one_hundreds = safe_int(one_hundred_entry)

            ones_total = ones * (2 if st.session_state.conversion_multiplier == 2 else 1)
            cash_chip_total = 0
            non_cash_total = ones_total

            if st.session_state.conversion_multiplier == 5:
                non_cash_total += fives * 5
            else:
                cash_chip_total += fives * 5

            if st.session_state.conversion_multiplier == 25:
                non_cash_total += twenty_fives * 25
            else:
                cash_chip_total += twenty_fives * 25

            cash_chip_total += one_hundreds * 100
            total_input = cash_chip_total + non_cash_total

            st.session_state.show_result = True
            st.session_state.correct = False

            if st.session_state.change_enabled:
                if total_input != st.session_state.correct_answer:
                    st.error(f"Incorrect. Total entered: £{total_input}")
                elif cash_chip_total != st.session_state.required_cash_change:
                    st.error(f"Incorrect. Cash should be exactly: £{st.session_state.required_cash_change}")
                else:
                    st.success(f"Correct! Total: £{total_input} - Press enter to recieve a new question")
                    st.session_state.correct = True
            else:
                if total_input == st.session_state.correct_answer:
                    st.success(f"Correct! Total: £{total_input} - Press enter to recieve a new question")
                    st.session_state.correct = True
                else:
                    st.error(f"Incorrect. Total entered: £{total_input}")

    if st.session_state.show_result:
        if st.session_state.show_answer:
            st.info(f"💡 The correct answer is £{st.session_state.correct_answer}")


    new_question, show_answer, return_to_menu = st.columns(3)

    if new_question.button("New Question", use_container_width=True):
        reset_question()

    show_answer.button("Show Answer", use_container_width=True, disabled=st.session_state.show_answer, on_click=reveal_question)
    
    if return_to_menu.button("Return to Menu", use_container_width= True):
        st.session_state.clear()
        st.switch_page("pages/roulette_payouts.py")
