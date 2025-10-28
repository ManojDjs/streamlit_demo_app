import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, about, dashboard
import numpy as np
import time
# --- Simulated DB data ---
questions = np.array([
    {"id": 1, "question_text": "What is 2 + 2?", "options": ["3", "4", "5"]},
    {"id": 2, "question_text": "What is the capital of Italy?", "options": ["Rome", "Paris", "Madrid"]},
    {"id": 3, "question_text": "Who wrote 'Hamlet'?", "options": ["Shakespeare", "Hemingway", "Twain"]},
])
# --- APP CONFIG ---
st.set_page_config(
    page_title="Multi-Page Streamlit App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Initialize session ---
if "questions" not in st.session_state:
    st.session_state.questions = questions.copy()
if "next_id" not in st.session_state:
    st.session_state.next_id = len(st.session_state.questions) + 1

def add_new_question():
    """Add a new question dynamically."""
    new_text = st.session_state.new_question_text.strip()
    if new_text:
        new_q = {"id": st.session_state.next_id, "question_text": new_text}
        st.session_state.questions = np.append(
                        st.session_state.questions,
                        np.array([new_q])
)
        st.session_state.next_id += 1
        st.session_state.new_question_text = ""  # clear input
        st.toast(f"➕ Added new question: '{new_text}'")
    else:
        st.warning("Please enter a valid question before adding.")
# -------------------------------
# ✅ Isolated business logic
# -------------------------------
def update_question(idx: int):
    """Update question text in session_state when user edits text box."""
    key = f"q_text_{idx}"
    new_value = st.session_state[key]
    st.session_state.questions[idx]["question_text"] = new_value

def make_update_callback(idx, field, key, option_index=None):
    def _callback():
        new_val = st.session_state[key]
        update_question(idx, field, new_val, option_index)
    return _callback

def process_question(idx: int):
    """Simulate long-running task and show progress."""
    q_text = st.session_state.questions[idx]["question_text"]

    # Create an empty placeholder for the progress bar
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0, text=f"Processing Question {idx + 1}...")

    # Simulate delay with incremental updates
    for percent in range(100):
        time.sleep(0.02)  # total ~2 seconds
        progress_bar.progress(percent + 1, text=f"Processing Question {idx + 1}...")

    # Remove progress bar after completion
    progress_placeholder.empty()

    # Toast message after delay
    st.toast(f"✅ Done processing Question {idx + 1}: '{q_text}'")
# --- TOP NAVBAR ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Dashboard", "About"],
    icons=["house", "bar-chart", "info-circle"],
    orientation="horizontal",
    default_index=0,
)

st.session_state.page = selected

# --- SIDEBAR CONTENT ---
st.sidebar.title("App Controls")

st.sidebar.markdown("### Global Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
username = st.sidebar.text_input("Enter your name", "User")

# Store state values
st.session_state.theme = theme
st.session_state.username = username

st.sidebar.write("Current page:", st.session_state.page)

# --- ROUTING ---
if st.session_state.page == "Home":
    home.render()

    @st.fragment
    def question_fragment(idx: int):
        """Fragment UI for editing one question."""
        q = st.session_state.questions[idx]
        st.subheader(f"Question #{idx + 1}")

        # Text box with on_change callback
        st.text_input(
            "Edit question:",
            value=q["question_text"],
            key=f"q_text_{idx}",
            on_change=update_question,
            args=(idx,)
        )
        # Process button → calls isolated function
        if st.button(f"Process Question {idx + 1}", key=f"process_btn_{idx}"):
            process_question(idx)
        

        st.write(f"📝 Current text: **{st.session_state.questions[idx]['question_text']}**")
        st.divider()
    # -------------------------------
# ➕ Add new question section
# -------------------------------
    # Temporary key for input
    input_key = "temp_new_question"

    # Text input
    new_question_text = st.text_input(
        "Enter new question:",
        value="",
        key=input_key,
        placeholder="Type a new question here..."
    )

    # Add button
    if st.button("➕ Add Question"):
        if new_question_text.strip():
            # Append new question to session
            st.session_state.questions = np.append(
                st.session_state.questions,
                np.array([{
                    "id": st.session_state.next_id,
                    "question_text": new_question_text.strip()
                }])
            )
            st.session_state.next_id += 1

            
            st.toast(f"Added question: '{new_question_text.strip()}'")
        else:
            st.warning("Please enter a valid question.")

        st.write("---")
    # ----------------------------------------------------
    # 🔁 Render all questions
    # ----------------------------------------------------
    for i in range(len(st.session_state.questions)):
        question_fragment(i)
elif st.session_state.page == "Dashboard":
    dashboard.render()
elif st.session_state.page == "About":
    about.render()
