from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
import streamlit as st
llm=ChatGroq(model="openai/gpt-oss-120b")
# que="what is the capital of india?"
# result=llm.invoke(que)
# print(result.content)

# while True:

#     que=input("Enter your question: ")
#     if que.lower in ["exit", "quit"]:
#         break


#     result=llm.invoke(que)
#     print(result.content)

st.title("AskBuddy QnA Bot");
st.markdown("This is a simple QnA bot using langchain-groq and streamlit. You can ask any question and get the answer from the model.")

#data store
if "messages" not in st.session_state:
    st.session_state["messages"] = []
for message in st.session_state.messages:
   role=message["role"]
   content=message["content"]
   st.chat_message(role).markdown(content)

query=st.chat_input("Ask a question")

if query:
   st.session_state.messages.append({"role": "user", "content": query})
   st.chat_message("user").markdown(query)
   res=llm.invoke(query)
   st.chat_message("assistant").markdown(res.content)
   st.session_state.messages.append({"role": "assistant", "content": res.content})