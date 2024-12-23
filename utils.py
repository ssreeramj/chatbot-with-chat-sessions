import streamlit as st

def initialize_new_chat():
    """
    function to initialize a new chat session
    """
    st.session_state.messages = [{"role": "ai", "content": "How can I help you today?"}]