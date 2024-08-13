import streamlit as st
from Groq_model import llm_model, clear_session_history
from groq import AuthenticationError
import os
import uuid

# Check for API key
if "GROQ_API_KEY" in os.environ:
    st.session_state.api_key = os.environ["GROQ_API_KEY"]

if "api_key" not in st.session_state:
    st.session_state.api_key = None

def request_api_key():
    st.sidebar.warning("Groq API Key not found or invalid.")
    api_key = st.sidebar.text_input("Please enter your Groq API Key:", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.sidebar.success("API Key set successfully!")
        st.session_state.messages = []
        st.rerun()
    else:
        st.sidebar.error("Please provide a valid API Key to continue.")
        st.stop()

if not st.session_state.api_key:
    request_api_key()

st.title("Chatbot")

st.sidebar.header("About This Bot")
st.sidebar.write(
    """
    **Chatbot** is designed to assist you with various queries. 
    It uses advanced AI to understand and respond to your messages.
    Feel free to ask anything or clear the chat history if needed.
    """
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Sidebar options
if st.sidebar.button("Clear Chat History"):
    clear_session_history(st.session_state.conversation_id)
    st.session_state.messages = []
    st.sidebar.success("Chat history cleared!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response
if prompt := st.chat_input("Write your message here..."):
    try:
        with_message_history = llm_model(st.session_state.api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            stream = with_message_history.stream(
                {"ability": "general", "question": prompt},
                config={"configurable": {"conversation_id": st.session_state.conversation_id}}
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except AuthenticationError as e:
        st.error("Authentication Error: Invalid API Key. Please check your Groq API key and try again.")
        st.error(f"Error details: {str(e)}")
        st.session_state.api_key = None
        request_api_key()

# Download button for chat history
if st.session_state.messages:
    chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.sidebar.download_button(
        label="Download Chat History",
        data=chat_history,
        file_name="chat_history.txt",
        mime="text/plain"
    )