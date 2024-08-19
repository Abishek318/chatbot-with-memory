# Chatbot with Memory

![Chatbot with Memory](path/to/your/sample/image.png)

A conversational AI chatbot designed to retain context and remember previous interactions, providing more personalized and coherent responses over time.

## Live Demo

Try out the live demo of the chatbot here: [https://mindfull-chatbot.streamlit.app/](https://mindfull-chatbot.streamlit.app/)

## Features

- Persistent memory across conversations
- Integration with Groq's large language model
- Streamlit-based user interface

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Abishek318/chatbot-with-memory.git
   cd chatbot-with-memory
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Groq API key:
   - Option 1: Set an environment variable:
     ```
     export GROQ_API_KEY=your_api_key_here
     ```
   - Option 2: Enter the API key in the Streamlit sidebar when prompted.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:2000`).

3. If you haven't set an environment variable for the API key, enter it in the sidebar when prompted.

4. Start chatting with the bot! Your conversation history will be maintained across sessions.

5. Use the "Clear Chat History" button in the sidebar to start a new conversation.

6. Download your chat history using the "Download Chat History" button in the sidebar.

## How It Works

This chatbot utilizes Groq's large language model to generate responses. It maintains conversation context using an in-memory storage system, allowing for more coherent and contextually relevant interactions over time.

The user interface is built with Streamlit, providing an easy-to-use chat interface. The bot's responses are streamed in real-time, creating a dynamic conversational experience.
