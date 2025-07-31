import os
import requests
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Constants
push_over_app_text_msg = "Hi there, this is a message from Karthic. Pushover app works fine and I love it!"

def chatollama_tool():
    llm = ChatOllama(model='llama3.2') # YOUR MODEL HERE can be llama2 or llama3.2...
    # Without bind.
    chain = (
        llm
        | StrOutputParser()
    )
    print(chain.invoke("Repeat quoted words exactly: 'One two three four five.'"))  # Output is 'One two three four five.'
    # With bind.
    chain = (
        llm.bind(stop=["three"])
        | StrOutputParser()
    )
    print(chain.invoke("Repeat quoted words exactly: 'One two' three four five.'")) # Output is 'One two'

def pushover_tool(text_msg: str):
    # Load pushover tool configurations
    load_dotenv(override=True)
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_url = "https://api.pushover.net/1/messages.json"
    print("Sending text message to your mobile...")
    """Send a push notification to the user"""
    requests.post(pushover_url, data={"token": pushover_token, "user": pushover_user, "message": text_msg})
    print("Text message was sent to your mobile successfully!")

if __name__ == "__main__":
    # Call all tools
    chatollama_tool()
    pushover_tool(push_over_app_text_msg)
