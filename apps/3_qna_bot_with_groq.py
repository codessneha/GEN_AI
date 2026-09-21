#LLM
#TOOL=GOOGLE SEARCH
#AGENT
#MEMORY
#STREAMING
#WEB INTERFACE

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    streaming=True
)
search=GoogleSerperAPIWrapper()
tools=[search.run]

if "memory" not in st.session_state:
  st.session_state.memory=MemorySaver()
  st.session_state.history=[]

agent=create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful assistant that can answer questions using Google search results."
)

#buiuld web interface
st.subheader("QuickAnswer-Answers at the speed of thought.")
for message in st.session_state.history:
    role=message["role"]
    content=message["content"]
    st.chat_message(role).markdown(content)

query=st.chat_input("Ask Anything?")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})
    response=agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    {"configurable":{"thread_id":"1"}},
    stream_mode="messages"
)
    ai_container=st.chat_message("assistant")
    with ai_container:
       space=st.empty()
       messages=""
       for chunk in response:
            messages=messages+chunk[0].content
            space.write(messages)
    
    st.session_state.history.append({"role":"assistant","content":messages})
    # st.chat_message("assistant").markdown(ans)




