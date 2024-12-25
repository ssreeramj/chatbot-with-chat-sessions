import os
import time
from glob import glob
from pathlib import Path

import joblib
import streamlit as st
from rich.console import Console
from rich.pretty import pprint
import json

console = Console()


def create_folder_if_not_exists(folder_path: str = "chat-sessions") -> None:
    """
    Create a folder if it doesn't already exist.

    Args:
        folder_path (str): The path of the folder to create.
    """
    try:
        os.mkdir(folder_path)
        console.log(f"{folder_path} folder created", style="green")
    except FileExistsError:
        console.log(f"{folder_path} folder already exists", style="yellow")


def load_past_chat_sessions(dir="chat-sessions", file_name="chat-id-mappings"):
    """
    Load past chats from the data folder.
    """
    try:
        chat_sessions: dict = joblib.load(Path(__file__).parent / dir / file_name)
    except FileNotFoundError:
        console.log("No past chat sessions found", style="yellow")
        chat_sessions = {}
    except Exception as e:
        console.print_exception()
        st.stop()

    return chat_sessions


def save_chat_session(dir_name="chat-sessions"):
    """
    Save the chat session to disk.
    """
    if "messages" in st.session_state:
        if len(st.session_state.messages) > 2:
            joblib.dump(
                st.session_state.messages,
                Path(__file__).parent / dir_name / f"{st.session_state.chat_id}",
            )

            # dump the session id-name mapping dictionary
            joblib.dump(
                st.session_state.chat_sessions,
                Path(__file__).parent / dir_name / "chat-id-mappings",
            )


def initialize_new_chat():
    """
    function to initialize a new chat session
    """
    # todo: save the mapping and the chat session both
    # check if there is any user message in session state

    save_chat_session()

    st.session_state.chat_id = f"{time.time()}"

    # Load past chats (if available)
    st.session_state.chat_sessions = load_past_chat_sessions()
    st.session_state.selectbox_options = [st.session_state.chat_id] + sorted(
        list(st.session_state.chat_sessions.keys()), key=float, reverse=True
    )
    # st.session_state.chat_session_selectbox = st.session_state.chat_id

    if "chat_title" in st.session_state:
        del st.session_state["chat_title"]

    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

    console.print("New chat session initialized", style="blue bold")


def generate_chat_session_name(user_input: str, model) -> str:
    """
    function to generate a unique chat session name
    from the user question.
    """
    prompt = f"Given a user question, return just 3-4 words that could be used as a chat title. Just return a single chat title, dont return multiple options.\n\nUser Question: {user_input}"
    response = model.generate_content(prompt)
    console.print(f"Generated chat title: {response.text}", style="blue")
    st.session_state.chat_title = response.text
    st.session_state.chat_sessions[st.session_state.chat_id] = response.text


def format_chat_history():
    """
    function to take message from session state and pass
    the entire history as prompt to the model
    """
    prompt = "You are a helpful AI assistant. Given below the conversion with the human, answer in the most helpful way possible.\n"
    for message in st.session_state.messages[1:][-5:]:
        if message["role"] == "user":
            prompt += f"User: {message['content']}\n"
        else:
            prompt += f"AI: {message['content']}\n"

    return prompt + "AI: "


def select_chat_session():
    """
    function to select a chat session
    """
    console.print("Selectbox updated", style="bold blue")
    # save the current chat session if valid
    save_chat_session()

    # get the selectoin from selectbox
    # assign chat id
    if st.session_state.chat_id != st.session_state.chat_session_selectbox:
        st.session_state.chat_id = st.session_state.chat_session_selectbox

        st.session_state.selectbox_options = [st.session_state.chat_id] + sorted(
            [
                opt
                for opt in st.session_state.selectbox_options
                if opt != st.session_state.chat_id
            ],
            key=float,
            reverse=True,
        )

        # assign chat title
        st.session_state.chat_title = st.session_state.chat_sessions.get(
            st.session_state.chat_id
        )
        # assign messages
        # check if the switch is to a new chat
        try:
            st.session_state.messages = joblib.load(
                Path(__file__).parent / "chat-sessions" / st.session_state.chat_id
            )
        except FileNotFoundError:
            st.session_state.messages = [
                {"role": "assistant", "content": "How can I help you today?"}
            ]
        except:
            console.print_exception()
            st.stop()

