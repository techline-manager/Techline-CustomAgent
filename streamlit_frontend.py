import streamlit as st
import streamlit_backend as st_be
import json

# Configure the page
st.set_page_config(
    page_title="Techline Customer Chat",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
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

    
# Sidebar controls
st.sidebar.header("🎛️ Controls")

if st.sidebar.button("🚀 Start New Conversation", type="primary"):
    st_be.start_conversation()

if st.sidebar.button("📋 Get Conversation Data"):
    history = st_be.get_conversation_history()
    if history:
        st.sidebar.success(f"📊 **Conversation Stats:**")
        st.sidebar.write(f"- Total messages: {history['total_messages']}")
        st.sidebar.write(f"- Address validated: {'✅' if history['thread_state']['address_validated'] else '❌'}")

# API Status check
with st.sidebar.expander("🔍 API Status"):
    if st.button("Check API Health"):
        success, response = st_be.make_api_request("health")
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
                    st_be.validate_address(address_input.strip())
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
                    st_be.send_chat_message(chat_input.strip())
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

