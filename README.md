# Streamlit Gemini Chatbot with sessions

This project demonstrates how to build a chatbot using Streamlit and Google's Generative AI model. The chatbot can save and load past chat sessions, generate chat session names, and provide helpful responses to user inputs.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/rag-with-sources-tutorial.git
    cd rag-with-sources-tutorial
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add your Google API key:

    ```env
    GOOGLE_API_KEY=<your_google_api_key>
    ```

## Usage

1. **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

2. **Interact with the chatbot:**

    Open your browser and go to `http://localhost:8501` to interact with the chatbot. You can start a new chat session, view past sessions, and get responses from the AI model.

## Project Structure

```
chatbot-with-chat-sessions/
├── app.py
├── utils.py
├── requirements.txt
├── .env.example
├── README.md
└── chat-sessions/
```

- `app.py`: Main application file that sets up the Streamlit interface and handles user interactions.
- `utils.py`: Utility functions for managing chat sessions, formatting chat history, and generating chat session names.
- `requirements.txt`: List of Python dependencies required for the project.
- `.env.example`: Example environment file to set up your API keys.
- `README.md`: This file.
- `chat-sessions/`: Directory to store chat session data.

## Features

- **Chatbot Interface:** A user-friendly interface to interact with the chatbot.
- **Session Management:** Save and load past chat sessions.
- **Dynamic Chat Titles:** Generate unique chat session names based on user input.
- **Streaming Responses:** Display AI responses in a streaming manner for a more interactive experience.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the project's coding standards and includes appropriate tests.
