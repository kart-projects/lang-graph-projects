import os
import random
from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class State(BaseModel): 
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Whether to override the system environment variables with the variables in the .env file
load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-4o-mini")

# Step 3: Create a Node
def chatbot_node(oldstate: State) -> State:
    response = llm.invoke(oldstate.messages)
    new_state = State(messages=[response])
    return new_state

graph_builder.add_node("chatbot", chatbot_node)

# Step 4: Create Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Step 5: Compile the Graph
graph = graph_builder.compile()

def chat(user_input: str, history):
    initial_state = State(messages=[{"role": "user", "content": user_input}])
    result = graph.invoke(initial_state)
    print(result)
    return result['messages'][-1].content

gr.ChatInterface(chat, type="messages").launch()