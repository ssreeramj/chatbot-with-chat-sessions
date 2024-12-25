import os
import time

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from rich.console import Console

from utils import (
    create_folder_if_not_exists,
    format_chat_history,
    generate_chat_session_name,
    initialize_new_chat,
    select_chat_session,
)

console = Console()
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
)

st.title("🤖 Chatbot with Chat Sessions")

# Set OpenAI API key from Streamlit secrets
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# create data folder to store chat sessions
create_folder_if_not_exists("chat-sessions/")

# Initialize new chat session
if "messages" not in st.session_state:
    initialize_new_chat()


# Sidebar
with st.sidebar:
    st.write("## Historical Chat Sessions")

    st.selectbox(
        label="Select a chat session",
        options=st.session_state.selectbox_options,
        format_func=lambda x: st.session_state.chat_sessions.get(x, "New Chat"),
        placeholder="_",
        key="chat_session_selectbox",
        on_change=select_chat_session,
        help="You can resume any historical chat session or start a new one",
    )

    st.divider()

    st.button(
        "New Chat 📝",
        help="Click to start a new chat session",
        on_click=initialize_new_chat,
    )


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)
        if len(st.session_state.messages) < 2:
            generate_chat_session_name(
                user_input=prompt,
                model=model,
            )

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        formatted_prompt = format_chat_history()
        response = model.generate_content(formatted_prompt, stream=True)

        # display streaming response
        ai_msg_placeholder = st.empty()
        full_response = ""
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            for ch in chunk.text.split(" "):
                full_response += ch + " "
                time.sleep(0.05)
                # Rewrites with a cursor at end
                ai_msg_placeholder.write(full_response + "|")

        # Write full message with placeholder
        ai_msg_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
