import streamlit as st
import random
import time

st.set_page_config(page_title="Multiplication Tables")

# -------------------
# Mode selection
# -------------------
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False
    st.session_state.mode = None

if not st.session_state.mode_selected:
    st.markdown("<h1 style='text-align: center;'>Multiplication Tables</h1>", unsafe_allow_html=True)

    left, middle, right = st.columns(3, vertical_alignment="center")

    launch_5 = middle.button("5", use_container_width=True)
    launch_6 = middle.button("6", use_container_width=True)
    launch_8 = middle.button("8", use_container_width=True)
    launch_9 = middle.button("9", use_container_width=True)
    launch_11 = middle.button("11", use_container_width=True)
    launch_17 = middle.button("17", use_container_width=True)
    launch_35 = middle.button("35", use_container_width=True)
    return_to_menu = middle.button("Return to Main Menu", use_container_width=True)

    for mode, button in [
        (5, launch_5),
        (6, launch_6),
        (8, launch_8),
        (9, launch_9),
        (11, launch_11),
        (17, launch_17),
        (35, launch_35),
    ]:
        if button:
            st.session_state.mode_selected = True
            st.session_state.mode = mode
            st.rerun()

    if return_to_menu:
        st.session_state.clear()
        st.switch_page("main.py")

else:
    # -------------------
    # Question + options generators
    # -------------------
    def generate_all_questions(multiplier: int, upto: int = 20):
        #Return shuffled list of dicts with prompt, answer, options.
        questions = []
        for i in range(1, upto + 1):
            prompt = f"{i} × {multiplier}"
            answer = i * multiplier
            options = generate_options(i, multiplier, answer)
            questions.append({"prompt": prompt, "answer": answer, "options": options})
        random.shuffle(questions)
        return questions

    def generate_options(i: int, m: int, correct: int):
        #Generate 3 plausible wrong answers and shuffle with correct one.
        candidates = set()

        if i > 1:
            candidates.add((i - 1) * m)
        candidates.add((i + 1) * m)
        if m > 1:
            candidates.add(i * (m - 1))
        candidates.add(i * (m + 1))

        candidates.discard(correct)
        candidates = {c for c in candidates if c > 0}

        while len(candidates) < 3:
            delta = random.choice([-3, -2, -1, 1, 2, 3]) * max(1, m // 5)
            cand = correct + delta
            if cand > 0 and cand != correct:
                candidates.add(cand)

        distractors = random.sample(list(candidates), 3)
        options = distractors + [correct]
        random.shuffle(options)
        return options

    # -------------------
    # Initialize quiz state once
    # -------------------
    if "questions" not in st.session_state:
        st.session_state.questions = generate_all_questions(st.session_state.mode)
        st.session_state.current_index = 0
        st.session_state.correct_count = 0
        st.session_state.selected = None  # stores last choice

    total_q = len(st.session_state.questions)
    idx = st.session_state.current_index

    if idx < total_q:
        q = st.session_state.questions[idx]

        st.markdown(f"<h1 style='text-align: center;'>Multiplying by {st.session_state.mode}</h1>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center; font-size:64px; font-weight:700; margin: 0.25rem 0 1rem 0;'>{q['prompt']}</div>",
            unsafe_allow_html=True,
        )

        st.progress(idx / total_q)
        st.caption(f"Question {idx + 1} of {total_q}")

        left, middle, right = st.columns(3)

        if left.button("Return to Menu", use_container_width=True):
            st.session_state.clear()
            st.switch_page("pages/multiplication_tables.py")

        # If user just answered, show feedback first
        if st.session_state.selected is not None:
            chosen = st.session_state.selected
            correct = q["answer"]

            # Build styled buttons (disabled)
            cols = st.columns(2)
            for j, opt in enumerate(q["options"]):
                style = ""
                if opt == correct:
                    style = "background-color: #4CAF50; color: white; font-weight: bold;"  # green
                elif opt == chosen:
                    style = "background-color: #F44336; color: white; font-weight: bold;"  # red

                button_html = f"""
                <div style="margin: 4px;">
                    <button disabled style="width:100%; padding:5px; border-radius:8px; {style}">
                        {opt}
                    </button>
                </div>
                """
                cols[j % 2].markdown(button_html, unsafe_allow_html=True)

            # Update score
            if chosen == correct:
                st.session_state.correct_count += 1

            # Move on after short pause
            time.sleep(0.5)
            st.session_state.current_index += 1
            st.session_state.selected = None
            st.rerun()
        
        else:
            # Normal answering phase
            cols = st.columns(2)
            for j, opt in enumerate(q["options"]):
                if cols[j % 2].button(str(opt), use_container_width=True, key=f"opt_{idx}_{j}"):
                    st.session_state.selected = opt
                    st.rerun()

    else:
        # Finished
        st.success(
            f"🎉 Completed the ×{st.session_state.mode} multiplication table! "
            f"Score: {st.session_state.correct_count}/{total_q}"
        )
        st.progress(1.0)

        c1, c2 = st.columns(2)
        if c1.button("Try again", use_container_width=True):
            del st.session_state.questions
            del st.session_state.current_index
            del st.session_state.correct_count
            del st.session_state.selected
            st.rerun()

        if c2.button("Return to Menu", use_container_width=True):
            st.session_state.clear()
            st.switch_page("pages/multiplication_tables.py")
