import streamlit as st
from google.cloud import dialogflowcx_v3beta1 as dialogflowcx
import uuid
import os
import json

# Load credentials (you can also use environment variable instead of file)
SERVICE_ACCOUNT_FILE = "service_account.json"
PROJECT_ID = "aichatbot-459310"
LOCATION = "us-central1"
AGENT_ID = "c332d7e4-2fea-4602-921e-c9894af54958"
LANGUAGE_CODE = "en"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE

@st.cache_resource
def get_session_client():
    return dialogflowcx.SessionsClient()

def detect_intent_texts(text_input, session_id):
    client = get_session_client()
    session_path = client.session_path(PROJECT_ID, LOCATION, AGENT_ID, session_id)

    text_input_obj = dialogflowcx.TextInput(text=text_input)
    query_input = dialogflowcx.QueryInput(
        text=text_input_obj,
        language_code=LANGUAGE_CODE
    )

    request = dialogflowcx.DetectIntentRequest(
        session=session_path,
        query_input=query_input
    )

    response = client.detect_intent(request=request)
    return response.query_result.response_messages

# --- Streamlit UI ---
st.set_page_config(page_title="GCP Bot in Streamlit", page_icon="🤖")
st.title("💬 Chat with GCP Dialogflow CX Bot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_responses = detect_intent_texts(user_input, st.session_state.session_id)

    for msg in bot_responses:
        text = msg.text.text[0] if msg.text.text else ""
        st.session_state.chat_history.append(("Bot", text))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.write(f"**{speaker}:** {message}")
