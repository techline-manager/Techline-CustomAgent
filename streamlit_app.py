import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="Techline Customer Chat",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
API_BASE_URL = st.sidebar.text_input(
    "API Base URL", 
    value="http://localhost:8000",
    help="Enter your API base URL (local or GCP Cloud Run URL)"
)

st.title("🏠 Techline Cleaning Services")
st.subheader("Customer Service Chat Interface")

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

def validate_address(address):
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

# Sidebar controls
st.sidebar.header("🎛️ Controls")

if st.sidebar.button("🚀 Start New Conversation", type="primary"):
    start_conversation()

if st.sidebar.button("📋 Get Conversation Data"):
    history = get_conversation_history()
    if history:
        st.sidebar.success(f"📊 **Conversation Stats:**")
        st.sidebar.write(f"- Total messages: {history['total_messages']}")
        st.sidebar.write(f"- Address validated: {'✅' if history['thread_state']['address_validated'] else '❌'}")

# API Status check
with st.sidebar.expander("🔍 API Status"):
    if st.button("Check API Health"):
        success, response = make_api_request("health")
        if success:
            st.success("✅ API is healthy")
            st.json(response)
        else:
            st.error("❌ API is not responding")
            st.error(response.get('error', 'Unknown error'))

# Main chat interface
if not st.session_state.conversation_started:
    st.info("👋 Welcome! Click **'Start New Conversation'** in the sidebar to begin.")
    st.markdown("""
    ### How it works:
    1. **Start a conversation** to get a thread ID
    2. **Provide your address or zip code** for validation
    3. **Chat with our AI assistant** about your cleaning needs
    
    The system ensures address validation before allowing conversations to proceed.
    """)
else:
    # Display conversation
    st.markdown("### 💬 Conversation")
    
    # Create a container for messages
    message_container = st.container()
    
    with message_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                st.caption(f"⏰ {msg['timestamp']}")
    
    # Input section
    st.markdown("---")
    
    if not st.session_state.address_validated:
        st.warning("📍 **Address Required**: Please provide your address or zip code to continue.")
        address_input = st.text_input(
            "Enter your address or zip code:",
            placeholder="e.g., 123 Main St, Anytown, CA 90210 or just 90210",
            key="address_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Validate Address", type="primary"):
                if address_input.strip():
                    validate_address(address_input.strip())
                else:
                    st.error("❌ Please enter an address or zip code.")
    else:
        st.success("🎉 **Address Validated!** You can now chat with our assistant.")
        
        # Chat input
        chat_input = st.text_input(
            "Your message:",
            placeholder="Tell us about your cleaning needs...",
            key="chat_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📤 Send", type="primary"):
                if chat_input.strip():
                    send_chat_message(chat_input.strip())
                else:
                    st.error("❌ Please enter a message.")

# Debug section (expandable)
if st.session_state.conversation_started:
    with st.expander("🔧 Debug Information"):
        st.write("**Session State:**")
        debug_info = {
            "Thread ID": st.session_state.thread_id,
            "Conversation Started": st.session_state.conversation_started,
            "Address Validated": st.session_state.address_validated,
            "Message Count": len(st.session_state.messages)
        }
        st.json(debug_info)
        
        if st.button("📥 Download Conversation JSON"):
            if st.session_state.conversation_history:
                st.download_button(
                    label="💾 Download JSON",
                    data=json.dumps(st.session_state.conversation_history, indent=2),
                    file_name=f"conversation_{st.session_state.thread_id}.json",
                    mime="application/json"
                )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🏠 Techline Cleaning Services | Powered by AI Assistant
    </div>
    """, 
    unsafe_allow_html=True
)
