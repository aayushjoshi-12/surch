import streamlit as st
from inference import get_answer

st.title("Surch:mag:...")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("What is up?"):
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    response = get_answer(question)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})