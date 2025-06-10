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

    if change_needed == "Enable":
        st.session_state.change_enabled = True
    else:
        st.session_state.change_enabled = False

    for multiplier, button in [(1, launch_1), (2, launch_2), (5, launch_5), (25, launch_25)]:
        if button:
            st.session_state.difficulty = difficulty
            st.session_state.difficulty_chosen = True
            st.session_state.conversion_multiplier = multiplier
            st.rerun()


    if return_to_menu:
        st.session_state.clear()
        st.switch_page("pages/roulette_menu.py")
else:
    # --------------------
    # Payout Logic
    # --------------------

    ALLOWED_CHIPS = {
    1: [1, 5, 25, 100],
    2: [1, 5, 25, 100],
    5: [5, 25, 100],
    25: [25, 100, 1000],
    }

    CHIP_IMAGES = {
    1: "assets/images/GreyChip.png",
    5: "assets/images/RedChip.png",
    25: "assets/images/BlackChip.png",
    100: "assets/images/PinkChip.png",
    1000: "assets/images/BlueChip.png",
    }

    # Question Pool - Default range set to Easy
    question_pool = DIFFICULTY_RANGES.get(st.session_state.difficulty, DIFFICULTY_RANGES["Easy"])
    
    def change_required():
        if st.session_state.conversion_multiplier == 2:
            return random.randrange(10, (st.session_state.correct_answer) + 1, 10)
        elif st.session_state.conversion_multiplier == 25:
            return random.randrange(100, (st.session_state.correct_answer) + 1, 100)
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
        st.session_state.trigger_autofocus = True

        for chip in [1, 5, 25, 100, 1000]:
            key_name = f"chip_key_{chip}"
        if key_name not in st.session_state:
            st.session_state[key_name] = f"chip_{chip}_{uuid.uuid4()}"

    if st.session_state.get("reset_inputs"):
        for chip in [1, 5, 25, 100, 1000]:
            st.session_state[f"chip_key_{chip}"] = f"chip_{chip}_{uuid.uuid4()}"
        st.session_state.reset_inputs = False
        st.session_state.trigger_autofocus = True

    st.markdown(f"<h1 style='text-align: center;'>Payout Simulator at £{st.session_state.conversion_multiplier}</h1>", unsafe_allow_html=True)
    st.subheader(f"{st.session_state.question_number} at {st.session_state.conversion_multiplier}")

    if st.session_state.change_enabled:
        st.write(f"Give exactly £{st.session_state.required_cash_change} in cash.")

    with st.form("answer_form"):


        allowed = ALLOWED_CHIPS.get(st.session_state.conversion_multiplier, [])
        chip_entries = {}
        
        cols = st.columns(len(allowed), vertical_alignment="center")

        for col, chip_value in zip(cols, allowed):
            with col:
                st.image(CHIP_IMAGES[chip_value])
                chip_key = st.session_state.get(f"chip_key_{chip_value}")
                chip_entries[chip_value] = st.number_input(
                    f"{chip_value} entry", 
                    label_visibility="collapsed", 
                    value=None, min_value=0, 
                    format="%d", 
                    step=5, 
                    key=chip_key,
                )

        submitted = st.form_submit_button("Check", type = "primary")

        if submitted:
            if st.session_state.correct:
                reset_question()

            used_chips = {chip: safe_int(chip_entries.get(chip, 0)) for chip in allowed}
            cash_chip_total = 0
            non_cash_total = 0

            for chip, count in used_chips.items():
                chip_value = chip

                # Special handling: if conversion is 2, 1-chip is worth 2
                if st.session_state.conversion_multiplier == 2 and chip == 1:
                    chip_value = 2

                if chip == st.session_state.conversion_multiplier:
                    non_cash_total += chip_value * count
                else:
                    cash_chip_total += chip_value * count

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

    #Removes enter to submit label text
    st.markdown(
        """
        <style>
        div[data-testid="InputInstructions"] > span:nth-child(1) {
        visibility: hidden;
        }
        </style>
        """,
            unsafe_allow_html=True
    )
    #Autofocus first input box
    if st.session_state.trigger_autofocus:
        st.components.v1.html(f"""
            <script>
                setTimeout(function() {{
                    const formInputs = window.parent.document.querySelectorAll('input[type="number"]');
                    if (formInputs.length > 0) {{
                        formInputs[0].focus();
                    }}
                }}, 150);  // longer delay to ensure DOM is ready
            </script>
        """, height=0)
        st.session_state.trigger_autofocus = False