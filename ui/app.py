import streamlit as st
import requests
from requests.exceptions import RequestException, JSONDecodeError

API_URL = "http://localhost:8000/api/chat"
REQUEST_TIMEOUT = 120  # Ollama can be slow on first run

st.set_page_config(
    page_title="Recommendation Chat",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Recommendation Assistant")

# -------------------------------
# Session state (chat memory)
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Render chat history
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat input (ChatGPT-like)
# -------------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:
    # --- Show user message immediately ---
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Call backend safely ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "user_message": prompt,
                        "user_id": 3,  # TODO: replace with real logged-in user
                        "language_code": "en",  # or "ko"
                    },
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code != 200:
                    st.error(f"Backend error ({response.status_code})")
                    st.text(response.text)
                    st.stop()

                data = response.json()
                reply = data.get("reply", "No reply received from backend.")

            except JSONDecodeError:
                st.error("Backend returned invalid JSON.")
                st.text(response.text)
                st.stop()

            except RequestException as e:
                st.error("Could not connect to backend.")
                st.text(str(e))
                st.stop()

        st.markdown(reply)

    # --- Save assistant message ---
    st.session_state.messages.append({"role": "assistant", "content": reply})
