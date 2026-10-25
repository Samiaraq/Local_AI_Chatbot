import streamlit as st
from chatbot import get_ai_response
import session_manager as sm

st.title("local AI chatbot")
st.sidebar.title("chat history")

new_chat= st.button("New Chat")

if new_chat or "session" not in st.session_state:
    st.session_state["session"]= sm.create_session()

for message in st.session_state["session"]["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt= st.chat_input("write your message ...")
if prompt :
    sm.add_message(
        st.session_state["session"],
        "user", 
        prompt
    )
    with st.chat_message("user"):
            st.write(prompt)
    response= get_ai_response(
        st.session_state["session"]["messages"])
    sm.add_message(
            st.session_state["session"],
            "assistant", 
            response
        )
    with st.chat_message("assistant"):
        st.write(response)
    sm.save_session(st.session_state["session"])

sessions=sm.get_all_sessions()
for session in sessions:
    if st.sidebar.button(
          session["title"],
          key=session["session_id"]
     ):
        st.session_state["session"]=sm.load_session(
            session["session_id"]
        )
        st.rerun()