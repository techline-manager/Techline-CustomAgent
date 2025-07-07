import os
import time
import json
from typing import Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from openai_api import OpenAI_API

from googlemaps_api import GoogleMapsAPI

load_dotenv()  # load .env file

# Get port from environment (GCP Cloud Run uses PORT env var)
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(
    title="Techline Custom Agent API",
    description="AI-powered cleaning service assistant with address validation",
    version="1.0.0"
)

@app.post("/start_conversation")
async def start_conversation():
    """Start a new conversation by asking for the user's address/zip code."""
    try:
        # Create a new thread
        thread = OpenAI_API.responses.threads.create()
        thread_id = thread.id
        
        # Ask for address/zip code
        initial_message = """Hello! Welcome to Techline cleaning services.

Before we can assist you with your cleaning needs, please provide either:
- Your complete address, or
- Your zip code

This helps us determine if we service your area and provide accurate pricing."""
        
        # Add the initial message to the thread
        OpenAI_API.responses.threads.messages.create(
            thread_id=thread_id,
            role="assistant",
            content=initial_message
        )
        
        return {
            "thread_id": thread_id,
            "message": initial_message,
            "requires_address": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting conversation: {str(e)}")

@app.post("/validate_address")
async def validate_address(request: Request):
    """Validate the user's address before allowing them to continue."""
    try:
        thread_id = request.thread_id
        address = request.address.strip()
        
        # Check if address looks like a zip code (5 digits) or full address
        if address.replace("-", "").isdigit() and len(address.replace("-", "")) in [5, 9]:
            # Validate zip code
            is_valid, location_data = GoogleMapsAPI.validate_zip_code(address)
            validation_type = "zip_code"
        else:
            # Validate full address
            is_valid, location_data = GoogleMapsAPI.validate_address(address)
            validation_type = "address"
        
        if is_valid:
            # Update thread state (thread-safe)

            # Add user's address to the thread
            OpenAI_API.responses.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=address
            )
            
            # Add confirmation message
            if validation_type == "zip_code":
                confirmation_msg = f"Great! I've confirmed that we service the {location_data['zip_code']} area"
                if location_data.get('city'):
                    confirmation_msg += f" in {location_data['city']}"
                if location_data.get('state'):
                    confirmation_msg += f", {location_data['state']}"
                confirmation_msg += ". How can I help you with your cleaning needs today?"
            else:
                confirmation_msg = f"Perfect! I've confirmed your address: {location_data['formatted_address']}. How can I help you with your cleaning needs today?"

            OpenAI_API.responses.threads.messages.create(
                thread_id=thread_id,
                role="assistant",
                content=confirmation_msg
            )
            
            return {
                "thread_id": thread_id,
                "address_valid": True,
                "address_data": location_data,
                "message": confirmation_msg,
                "can_continue": True
            }
        else:
            error_msg = "I'm sorry, but I couldn't validate that address or zip code. Please double-check and try again, or provide a different format (full address or 5-digit zip code)."
            
            OpenAI_API.responses.threads.messages.create(
                thread_id=thread_id,
                role="assistant",
                content=error_msg
            )
            
            return {
                "thread_id": thread_id,
                "address_valid": False,
                "message": error_msg,
                "can_continue": False
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating address: {str(e)}")

@app.post("/chat")
async def chat_with_assistant(request: Request):
    """Send a message to the assistant and get a response (only after address validation)."""
    try:
        thread_id = request.thread_id
        user_message = request.message

        # Add the user's message to the thread
        OpenAI_API.responses.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )
        
        # Create a run with the assistant
        run = OpenAI_API.responses.threads.runs.create(
            thread_id=thread_id,
            assistant_id=OpenAI_API.assistant_id
        )
        
        # Wait for the run to complete
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = OpenAI_API.responses.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status == 'completed':
            # Get the assistant's response
            messages = OpenAI_API.responses.threads.messages.list(thread_id=thread_id)
            assistant_response = messages.data[0].content[0].text.value
            
            return {
                "thread_id": thread_id,
                "user_message": user_message,
                "assistant_response": assistant_response,
                "run_id": run.id
            }
        else:
            raise HTTPException(status_code=500, detail=f"Assistant run failed with status: {run.status}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.get("/get_conversation/{thread_id}")
async def get_conversation_history(thread_id: str):
    """Get the latest conversation history from a thread."""
    try:
        # Get all messages from the thread
        messages = OpenAI_API.responses.threads.messages.list(thread_id=thread_id)

        conversation_history = []
        for message in reversed(messages.data):  # Reverse to get chronological order
            conversation_history.append({
                "role": message.role,
                "content": message.content[0].text.value,
                "timestamp": message.created_at
            })
        
        return {
            "thread_id": thread_id,
            "conversation_history": conversation_history,
            "total_messages": len(conversation_history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

@app.get("/thread_status/{thread_id}")
async def get_thread_status(thread_id: str):
    """Get the current status of a thread."""

    return {
        "thread_id": thread_id,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
