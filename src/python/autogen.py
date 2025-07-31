import asyncio
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken


async def autogen_tool():
    load_dotenv(override=True)

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini") # Modify and add your relevant model version as needed
    ollamamodel_client = OllamaChatCompletionClient(model="llama3.2") # Modify and add your relevant model version as needed

    message = TextMessage(content="I'd like to go to Washington D.C.", source="user")
    print(message)

    agent = AssistantAgent(
        name="airline_agent",
        model_client=model_client,
        system_message="You are a helpful assistant for an airline. You give short, humorous answers. Start answers with Hello World!!!",
        model_client_stream=True
    )

    response = await agent.on_messages([message], cancellation_token=CancellationToken())
    print(response.chat_message.content)

asyncio.run(autogen_tool())