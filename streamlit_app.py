import streamlit as st
import requests
import json
from datetime import datetime
import time

import openai
from open_ai_agent import get_openai_response


import os
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize session state
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "address_validated" not in st.session_state:
    st.session_state.address_validated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "awaiting_reply" not in st.session_state:
    st.session_state.awaiting_reply = False
if "trigger_reply" not in st.session_state:
    st.session_state.trigger_reply = False

# Configuration
API_BASE_URL = st.sidebar.text_input(
    "API Base URL", 
    value="https://openai-agent-service-test-327786004841.europe-southwest1.run.app",
    help="Enter your API base URL (local or GCP Cloud Run URL)"
)

def make_api_request(endpoint, method, data=None):
    """Make API request with error handling."""
    try:
        url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "Cannot connect to API. Make sure the server is running."}
    except requests.exceptions.Timeout:
        return False, {"error": "Request timed out. Please try again."}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}"}



def create_initial_page():
    st.set_page_config(
        page_title="Techline Customer Chat",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
   
def create_sidebar():
    """Create the sidebar with controls and information."""
    st.sidebar.header("🛠️ Controls")
    
    if st.sidebar.button("🚀 Start New Conversation", type="primary"):
        return 0
        # chat_interface()  # <-- Always show chat interface

    
    if st.sidebar.button("📋 Get Conversation Data"):
        history = st.session_state.get("conversation_history", None)
        if history:
            st.sidebar.success(f"📊 **Conversation Stats:**")
            st.sidebar.write(f"- Total messages: {history['total_messages']}")
            st.sidebar.write(f"- Address validated: {'✅' if history['thread_state']['address_validated'] else '❌'}")

def simulate_agent_typing(message, delay=0.05):
    typed = ""
    placeholder = st.empty()
    for char in message:
        typed += char
        placeholder.markdown(
            f"<div style='background-color:#147b94; padding:10px; border-radius:8px; margin-bottom:12px;'><b>Agent:</b> {typed}</div>",
            unsafe_allow_html=True
        )
        time.sleep(delay)
    return typed

def chat_interface():
    if "step_index" not in st.session_state:
        st.session_state.step_index = 0
    if "messages" not in st.session_state:
        st.session_state.messages = []

    current_step = st.session_state.step_index

    # 1. Handle user input FIRST
    user_input = st.chat_input("Your reply:", key=f"user_input_{current_step}")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.step_index += 1
        st.rerun()  # Immediately rerun to show update

    # 2. Render existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 3. Assistant prompts user if needed
    if current_step < len(assistant_prompts):
        if (
            len(st.session_state.messages) == 0
            or st.session_state.messages[-1]["role"] != "assistant"
        ):
            with st.chat_message("assistant"):
                st.markdown(assistant_prompts[current_step])
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_prompts[current_step]}
            )
            st.rerun()  # Immediately rerun to show update

def chat_interface_test_realbot():
    if "messages" not in st.session_state:
        # First turn: get assistant's first message
        st.session_state.messages = []
        assistant_msg = get_openai_response([])
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Your reply:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Rebuild OpenAI format:
        openai_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        assistant_msg = get_openai_response(openai_msgs)
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.rerun()

def chat_test_api_key():
    #Write truncated api key
    if api_key:
        truncated_key = api_key[:4] + "..." + api_key[-4:]
        st.sidebar.markdown(f"**API Key:** `{truncated_key}`")
    else:
        st.sidebar.error("API Key not set. Please set it in your environment variables.")

def create_footer():
    """Create the footer with additional information."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        🏠 Techline Cleaning Services | Powered by AI Assistant
        </div>
        """, 
        unsafe_allow_html=True
    )   

if __name__ == "__main__":
    counter = 0
    create_initial_page()
    chat_test_api_key()
    create_sidebar()
    create_footer()
