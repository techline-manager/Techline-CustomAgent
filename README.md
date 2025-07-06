# Techline Custom Agent

A conversational AI bot for Techline cleaning services customer service that validates addresses before starting conversations.

## Features

- **Address Validation**: Validates user addresses/zip codes using Google Maps API before allowing conversation
- **OpenAI Integration**: Uses OpenAI Assistant API for intelligent customer service responses
- **Thread Management**: Maintains conversation state and history
- **RESTful API**: FastAPI-based endpoints for easy integration

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

3. **Run the Server**:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### 1. Start Conversation
**POST** `/start_conversation`

Starts a new conversation and asks the user for their address/zip code.

**Response**:
```json
{
  "thread_id": "thread_xyz123",
  "message": "Hello! Welcome to Techline cleaning services...",
  "requires_address": true
}
```

### 2. Validate Address
**POST** `/validate_address`

Validates the user's address/zip code before allowing them to continue.

**Request Body**:
```json
{
  "address": "12345 Main St, Anytown, CA 90210",
  "thread_id": "thread_xyz123"
}
```

**Response** (Valid):
```json
{
  "thread_id": "thread_xyz123",
  "address_valid": true,
  "address_data": {
    "formatted_address": "12345 Main St, Anytown, CA 90210, USA",
    "location": {"lat": 34.0522, "lng": -118.2437},
    "place_id": "ChIJ..."
  },
  "message": "Perfect! I've confirmed your address...",
  "can_continue": true
}
```

### 3. Chat with Assistant
**POST** `/chat`

Send messages to the AI assistant (only after address validation).

**Request Body**:
```json
{
  "message": "I need a house cleaning quote",
  "thread_id": "thread_xyz123"
}
```

**Response**:
```json
{
  "thread_id": "thread_xyz123",
  "user_message": "I need a house cleaning quote",
  "assistant_response": "I'd be happy to help you with a cleaning quote...",
  "run_id": "run_abc456"
}
```

### 4. Get Conversation History
**GET** `/get_conversation/{thread_id}`

Retrieves the complete conversation history for a thread.

**Response**:
```json
{
  "thread_id": "thread_xyz123",
  "thread_state": {
    "address_validated": true,
    "address_data": {...},
    "conversation_started": true
  },
  "conversation_history": [
    {
      "role": "assistant",
      "content": "Hello! Welcome to Techline...",
      "timestamp": 1641234567
    },
    {
      "role": "user",
      "content": "90210",
      "timestamp": 1641234568
    }
  ],
  "total_messages": 4
}
```

### 5. Get Thread Status
**GET** `/thread_status/{thread_id}`

Gets the current status of a thread.

**Response**:
```json
{
  "thread_id": "thread_xyz123",
  "status": {
    "address_validated": true,
    "address_data": {...},
    "conversation_started": true
  }
}
```

## Usage Flow

1. **Start**: Call `/start_conversation` to begin
2. **Validate**: Use `/validate_address` with the user's address/zip code
3. **Chat**: Once validated, use `/chat` for normal conversation
4. **Monitor**: Use `/get_conversation/{thread_id}` to fetch conversation data for business logic

## Integration Example

```python
import requests

# Start conversation
response = requests.post("http://localhost:8000/start_conversation")
thread_data = response.json()
thread_id = thread_data["thread_id"]

# Validate address
address_response = requests.post("http://localhost:8000/validate_address", json={
    "address": "90210",
    "thread_id": thread_id
})

if address_response.json()["address_valid"]:
    # Now you can chat
    chat_response = requests.post("http://localhost:8000/chat", json={
        "message": "I need a cleaning quote",
        "thread_id": thread_id
    })
    
    # Get full conversation for business logic
    conversation = requests.get(f"http://localhost:8000/get_conversation/{thread_id}")
```

## Notes

- Address validation is required before any conversation can begin
- Thread states are maintained in memory (consider using a database for production)
- Google Maps API is used for address validation
- OpenAI Assistant API handles the conversational AI
