import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Page config
st.set_page_config(
    page_title="SparkChat ⚡",
    page_icon="⚡",
    layout="centered",
)

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .stChatMessage {
        padding: 0.5rem;
        border-radius: 10px;
    }
    .stChatMessage.user {
        background-color: #dbeafe;
    }
    .stChatMessage.assistant {
        background-color: #fef9c3;
    }
    .st-emotion-cache-16txtl3 {
        font-size: 1.2rem;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown(
    """
    <h1 style="text-align: center; color: #4F46E5; margin-bottom: 0;">
        ⚡ SparkChat
    </h1>
    <p style="text-align: center; color: #6B7280; margin-top: 0;">
        Your personal AI conversation partner, powered by OpenAI.
    </p>
    """,
    unsafe_allow_html=True
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

# User input
if user_prompt := st.chat_input("Ask me anything... 💬"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Optional footer credits
st.markdown(
    """
    <hr style="margin-top: 2em;">
    <p style="text-align: center; color: #9CA3AF;">
        ⚡ SparkChat — Powered by OpenAI
    </p>
    """,
    unsafe_allow_html=True
)
