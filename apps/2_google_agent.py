from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent


# LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


# Google Search tool
search = GoogleSerperAPIWrapper()


# Create agent
agent = create_agent(
    model=llm,
    tools=[search.run],
    system_prompt="You are a helpful assistant that can answer questions using Google search results."
)


# Chat loop
while True:

    query = input("Enter your query (or type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    print("AI:", response["messages"][-1].content)