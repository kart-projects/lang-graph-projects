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
import random

# Some useful constants
nouns = [
    "Snakes",
    "Scripts",
    "Lambdas",
    "Exceptions",
    "Modules",
    "Decorators",
    "Generators",
    "Packages",
    "Comprehensions",
    "Indentations"
]

adjectives = [
    "slithery",       # Snakes
    "ancient",        # Scripts
    "anonymous",      # Lambdas
    "catastrophic",   # Exceptions
    "modular",        # Modules
    "fancy",          # Decorators
    "lazy",           # Generators
    "bundled",        # Packages
    "clever",         # Comprehensions
    "rigid"           # Indentations
]

for adj, noun in zip(adjectives, nouns):
    print(f"The {adj} {noun}")

# Step 1: Define the State class (object)
# A word about "Annotated"
# You probably know this; type hinting is a feature in Python that lets you specify the type of something:
# `my_favorite_things: List`
# But you may not know this:
# You can also use something called "Annotated" to add extra information that somebody else might find useful:
# `my_favorite_things: Annotated[List, "these are a few of mine"]`
# LangGraph needs us to use this feature when we define our State object.
# It wants us to tell it what function it should call to update the State with a new value.
# This function is called a **reducer**.
# LangGraph provides a default reducer called `add_messages` which takes care of the most common case.
# And that hopefully explains why the State looks like this.
class State(BaseModel): 
    messages: Annotated[list, add_messages]

# Step 2: Start the Graph Builder with this State class
graph_builder = StateGraph(State)

# Step 3: Create a Node
# A node can be any python function.
# The reducer that we set before gets automatically called to combine this response with previous responses

def our_first_node(old_state: State) -> State:

    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    messages = [{"role": "assistant", "content": reply}]

    new_state = State(messages=messages)

    return new_state

graph_builder.add_node("first_node", our_first_node)

# Step 4: Create Edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

# Step 5: Compile the Graph
graph = graph_builder.compile()

# Step 6: Get the ascii string of the workflow image
print(graph.get_graph().draw_ascii())

png_image_data = Image(graph.get_graph().draw_mermaid_png())
with open("./src/resources/workflow_image.png", "wb") as f:
    f.write(png_image_data.data)
