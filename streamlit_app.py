import streamlit as st

# # memory store have two methods 
# # 1) Using a ChatModel
# # 2)using llm

# 1) Using a ChatModel and gemini
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv

load_dotenv()

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

store = {}

def get_session_history(conversation_id: str) -> BaseChatMessageHistory:
    if conversation_id not in store:
        store[conversation_id] = InMemoryHistory()
    return store[conversation_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | ChatGoogleGenerativeAI(model="gemini-1.5-flash")

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)


st.title("Chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("write here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = with_message_history.stream({"question": prompt},
            config={"configurable": {"conversation_id": "1"}}
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})