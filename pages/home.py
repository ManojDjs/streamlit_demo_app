import streamlit as st

def render():
    st.title("🏠 Home Page")
    st.write(f"Welcome, **{st.session_state.username}**!")
    st.write("This is the home page of your Streamlit multi-page app.")
    
    st.session_state.counter = st.session_state.get("counter", 0)
    if st.button("Increase Counter"):
        st.session_state.counter += 1
    st.write("Counter value:", st.session_state.counter)
