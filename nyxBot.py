from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# ------------------- STREAMLIT UI -------------------

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini 2.5 Flash")

# Sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.write("**Model:** gemini-2.5-flash")
    st.write("Built with Streamlit")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history using modern chat UI
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Chat input (modern replacement for text_input + button)
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = get_gemini_response(user_input)
        for chunk in response:
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.chat_history.append(("assistant", full_response))
