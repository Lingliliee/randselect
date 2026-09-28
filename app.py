import random
import time

import streamlit as st

from randselect.selector import random_selection, remaining_names

FLASH_SECONDS = 3
FLASH_INTERVAL = 0.1

st.title("Random Question Picker")

# --- state ---
defaults = {
    "names": [],
    "questions": [],
    "used_names": [],
    "result": None,
    "animate": False,
    "rng": random.Random(),
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

state = st.session_state

# --- inputs (event blocks mutate state only) ---
col_names, col_questions = st.columns(2)

with col_names:
    st.subheader("Roster")
    with st.form("add_name", clear_on_submit=True):
        new_name = st.text_input("Name")
        if st.form_submit_button("Add"):
            new_name = new_name.strip()
            if new_name and new_name not in state.names:
                state.names.append(new_name)
    st.caption(f"{len(state.names)} name(s)")
    for i, name in enumerate(state.names, 1):
        st.write(f"{i}. {name}")

with col_questions:
    st.subheader("Questions")
    with st.form("add_question", clear_on_submit=True):
        new_question = st.text_input("Question")
        if st.form_submit_button("Add"):
            new_question = new_question.strip()
            if new_question:
                state.questions.append(new_question)
    st.caption(f"{len(state.questions)} question(s)")
    for i, question in enumerate(state.questions, 1):
        st.write(f"{i}. {question}")

st.divider()

no_repeats = st.checkbox("No repeats", key="no_repeats")
pool = remaining_names(state.names, state.used_names) if no_repeats else state.names

can_draw = True
if not state.names or not state.questions:
    st.info("Add at least one name and one question.")
    can_draw = False
elif not pool:
    st.warning("All names are selected!")
    can_draw = False
    if st.button("Reset"):
        state.used_names = []
        state.result = None
        st.rerun()

if st.button("Draw", type="primary", disabled=not can_draw):
    state.result = random_selection(pool, state.questions, state.rng)
    if no_repeats:
        state.used_names.append(state.result[0])
    state.animate = True
    st.rerun()

# --- rendering (reads session state on every rerun) ---
placeholder = st.empty()

if state.animate:
    end = time.time() + FLASH_SECONDS
    while time.time() < end:
        name, question = random_selection(state.names, state.questions, state.rng)
        placeholder.markdown(f"### {name}, please answer: {question}")
        time.sleep(FLASH_INTERVAL)
    state.animate = False

if state.result:
    name, question = state.result
    placeholder.success(f"### **{name}**, please answer: {question}")

if no_repeats and state.used_names:
    st.caption("Already picked: " + ", ".join(state.used_names))
