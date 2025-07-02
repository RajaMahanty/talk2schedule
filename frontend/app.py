import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk", page_icon="🧵")

st.title("🧵 TailorTalk")
st.caption("Book appointments with ease via chat")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hi! How can I help you today?"}
    ]

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to FastAPI backend
    BACKEND_URL = "http://talk2schedule.railway.internal"
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": prompt}
        )
        result = response.json()["response"]
    except Exception as e:
        result = f"⚠️ Error: {e}"

    # Show AI response
    st.session_state.messages.append({"role": "ai", "content": result})
    with st.chat_message("ai"):
        st.markdown(result)
