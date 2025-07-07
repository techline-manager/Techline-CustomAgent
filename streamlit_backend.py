import streamlit as st
import requests
import json
from datetime import datetime
import time




def make_api_request(endpoint, method="GET", data=None):
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

def start_conversation():
    """Start a new conversation."""
    success, response = make_api_request("start_conversation", "POST")
    
    if success:
        st.session_state.thread_id = response["thread_id"]
        st.session_state.conversation_started = True
        st.session_state.address_validated = False
        st.session_state.messages = []
        
        # Add initial message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["message"],
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        st.success(f"✅ Conversation started! Thread ID: {st.session_state.thread_id}")
        st.rerun()
    else:
        st.error(f"❌ Failed to start conversation: {response.get('error', 'Unknown error')}")

def validate_address(address):1
    """Validate user's address."""
    if not st.session_state.thread_id:
        st.error("❌ No active conversation. Please start a conversation first.")
        return
    
    data = {
        "address": address,
        "thread_id": st.session_state.thread_id
    }
    
    success, response = make_api_request("validate_address", "POST", data)
    
    if success:
        if response["address_valid"]:
            st.session_state.address_validated = True
            
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": address,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["message"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            st.success("✅ Address validated successfully!")
            
            # Show address info in sidebar
            if "address_data" in response:
                addr_data = response["address_data"]
                st.sidebar.success("📍 **Validated Address:**")
                st.sidebar.write(f"**Address:** {addr_data.get('formatted_address', 'N/A')}")
                if "city" in addr_data:
                    st.sidebar.write(f"**City:** {addr_data['city']}")
                if "state" in addr_data:
                    st.sidebar.write(f"**State:** {addr_data['state']}")
                if "zip_code" in addr_data:
                    st.sidebar.write(f"**Zip Code:** {addr_data['zip_code']}")
        else:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": address,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Add error response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["message"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            st.error("❌ Address validation failed. Please try again.")
        
        st.rerun()
    else:
        st.error(f"❌ Validation failed: {response.get('error', 'Unknown error')}")

def send_chat_message(message):
    """Send a chat message to the assistant."""
    if not st.session_state.address_validated:
        st.error("❌ Please validate your address before chatting.")
        return
    
    data = {
        "message": message,
        "thread_id": st.session_state.thread_id
    }
    
    # Add user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Show loading message
    with st.spinner("🤖 Assistant is thinking..."):
        success, response = make_api_request("chat", "POST", data)
    
    if success:
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["assistant_response"],
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.rerun()
    else:
        st.error(f"❌ Chat failed: {response.get('error', 'Unknown error')}")
        # Remove the user message if the request failed
        st.session_state.messages.pop()
        st.rerun()

def get_conversation_history():
    """Fetch and display full conversation history."""
    if not st.session_state.thread_id:
        st.error("❌ No active conversation.")
        return
    
    success, response = make_api_request(f"get_conversation/{st.session_state.thread_id}")
    
    if success:
        st.session_state.conversation_history = response
        return response
    else:
        st.error(f"❌ Failed to get conversation history: {response.get('error', 'Unknown error')}")
        return None
