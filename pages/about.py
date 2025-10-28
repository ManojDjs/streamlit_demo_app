import streamlit as st

def render():
    st.title("ℹ️ About Page")
    st.write("This is a demo multi-page Streamlit app.")
    st.write("The app uses:")
    st.markdown("""
    - `st.session_state` for global state management  
    - `streamlit-option-menu` for the navbar  
    - Sidebar for global settings
    """)
