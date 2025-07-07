import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_flow():
    """Test the complete API flow."""
    
    
    # Step 1: Start conversation
    print("1. Starting conversation...")
    response = requests.post(f"{BASE_URL}/start_conversation")
    
    if response.status_code == 200:
        data = response.json()
        thread_id = data["thread_id"]
        print(f"✅ Conversation started")
        print(f"   Thread ID: {thread_id}")
        print(f"   Message: {data['message'][:100]}...")
        print()
    else:
        print(f"❌ Failed to start conversation: {response.status_code}")
        return
    
    # Step 2: Validate address (test with zip code)
    print("2. Validating address (zip code: 90210)...")
    address_response = requests.post(f"{BASE_URL}/validate_address", json={
        "address": "90210",
        "thread_id": thread_id
    })
    
    if address_response.status_code == 200:
        address_data = address_response.json()
        if address_data["address_valid"]:
            print("✅ Address validated successfully")
            print(f"   Location: {address_data['address_data']['formatted_address']}")
            print(f"   Message: {address_data['message'][:100]}...")
            print()
        else:
            print("❌ Address validation failed")
            print(f"   Message: {address_data['message']}")
            return
    else:
        print(f"❌ Address validation request failed: {address_response.status_code}")
        return
    
    # Step 3: Chat with assistant
    print("3. Chatting with assistant...")
    chat_response = requests.post(f"{BASE_URL}/chat", json={
        "message": "I need a house cleaning quote for a 3-bedroom house",
        "thread_id": thread_id
    })
    
    if chat_response.status_code == 200:
        chat_data = chat_response.json()
        print("✅ Chat successful")
        print(f"   User: {chat_data['user_message']}")
        print(f"   Assistant: {chat_data['assistant_response'][:150]}...")
        print()
    else:
        print(f"❌ Chat failed: {chat_response.status_code}")
        print(f"   Error: {chat_response.text}")
        return
    
    # Step 4: Get conversation history
    print("4. Retrieving conversation history...")
    history_response = requests.get(f"{BASE_URL}/get_conversation/{thread_id}")
    
    if history_response.status_code == 200:
        history_data = history_response.json()
        print("✅ Conversation history retrieved")
        print(f"   Total messages: {history_data['total_messages']}")
        print(f"   Address validated: {history_data['thread_state']['address_validated']}")
        print()
        
        print("📝 Full conversation:")
        for i, msg in enumerate(history_data['conversation_history'], 1):
            role_emoji = "🤖" if msg['role'] == 'assistant' else "👤"
            print(f"   {i}. {role_emoji} {msg['role'].title()}: {msg['content'][:100]}...")
        print()
    else:
        print(f"❌ Failed to get conversation history: {history_response.status_code}")
    
    # Step 5: Get thread status
    print("5. Checking thread status...")
    status_response = requests.get(f"{BASE_URL}/thread_status/{thread_id}")
    
    if status_response.status_code == 200:
        status_data = status_response.json()
        print("✅ Thread status retrieved")
        print(f"   Status: {json.dumps(status_data['status'], indent=2)}")
    else:
        print(f"❌ Failed to get thread status: {status_response.status_code}")
    
    print("\n🎉 API flow test completed!")

def test_invalid_scenarios():
    """Test invalid scenarios and error handling."""
    
    print("\n🧪 Testing error scenarios...\n")
    
    # Test chat without address validation
    print("1. Testing chat without address validation...")
    response = requests.post(f"{BASE_URL}/start_conversation")
    if response.status_code == 200:
        thread_id = response.json()["thread_id"]
        
        # Try to chat without validating address
        chat_response = requests.post(f"{BASE_URL}/chat", json={
            "message": "Hello",
            "thread_id": thread_id
        })
        
        if chat_response.status_code == 400:
            print("✅ Correctly blocked chat without address validation")
            print(f"   Error: {chat_response.json()['detail']}")
        else:
            print("❌ Should have blocked chat without address validation")
        print()
    
    # Test invalid address
    print("2. Testing invalid address...")
    response = requests.post(f"{BASE_URL}/start_conversation")
    if response.status_code == 200:
        thread_id = response.json()["thread_id"]
        
        # Try invalid address
        address_response = requests.post(f"{BASE_URL}/validate_address", json={
            "address": "INVALID_ADDRESS_123456",
            "thread_id": thread_id
        })
        
        if address_response.status_code == 200:
            data = address_response.json()
            if not data["address_valid"]:
                print("✅ Correctly identified invalid address")
                print(f"   Message: {data['message']}")
            else:
                print("❌ Should have rejected invalid address")
        print()

if __name__ == "__main__":
    try:
        # Test the main flow
        test_api_flow()
        
        # Test error scenarios
        test_invalid_scenarios()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
