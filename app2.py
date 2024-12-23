import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from utils import initialize_new_chat

load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(
    page_title="RAG Application",
    page_icon="📃",
    menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)

st.title("🤖 RAG")

# Set OpenAI API key from Streamlit secrets
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

with st.sidebar:
    st.button("New Chat :broom:", help="Click to start a new chat session", on_click=initialize_new_chat)

# Initialize chat history
if "messages" not in st.session_state:
    initialize_new_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = model.generate_content(prompt, stream=True)
        
        # display streaming response
        ai_msg_placeholder = st.empty()
        full_response = ''
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.02)
                # Rewrites with a cursor at end
                ai_msg_placeholder.write(full_response + '|')

        # Write full message with placeholder
        ai_msg_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
