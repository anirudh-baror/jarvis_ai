import streamlit as st
from ai.memory import init_db
from ai.gemini_client import ask_gemini

# Initialize the database (creates it if it doesn't exist)
init_db()

st.set_page_config(page_title="Jarvis AI", page_icon="🤖")
st.title("🤖 Jarvis AI Assistant")
st.caption("Chat with Jarvis in English, Hindi, or Hinglish")

# Keep chat messages in the browser session so they show up on screen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in this session
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Text input box at the bottom of the page
user_input = st.chat_input("Type your message to Jarvis...")

if user_input:
    # Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get Jarvis's response and show it
    with st.chat_message("assistant"):
        with st.spinner("Jarvis is thinking..."):
            response = ask_gemini(user_input)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})