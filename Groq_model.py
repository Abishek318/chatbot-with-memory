
# # memory store have two methods 
# # 1) Using a ChatModel
# # 2)using llm

# 1) Using a ChatModel and gemini
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

load_dotenv()

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)
    class Config:
        arbitrary_types_allowed = True

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

def clear_session_history(conversation_id: str) -> None:
    """Clear the message history for a given conversation."""
    if conversation_id in store:
        store[conversation_id].clear()
def delete_session(conversation_id: str) -> None:
    """Delete the session and its message history."""
    if conversation_id in store:
        del store[conversation_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer the user's questions clearly and accurately. Provide useful information and be polite. If you don't know the answer, let the user know and suggest where they might find more information."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])


def llm_model(api_key):
    chain = prompt | ChatGroq(api_key=api_key,model="llama-3.1-8b-instant")

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
    return with_message_history


# while True:
#     user_message=input("User: ")
#     if user_message!="exit":
#         rseponse=with_message_history.invoke(
#             {"question": user_message},
#             config={"configurable": {"conversation_id": "1"}}
#         )
#         print("Bot: ",rseponse.content)
#     else:
#         print("##conversation over...##")
#         break


