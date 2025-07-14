import os
import time
import streamlit_app as streamlit_app

from typing import Dict, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from open_ai_agent import AgentWrapper, agent, oa_client
from googlemaps_api import GoogleMapsAPI
from streamlit_app import render_chat_interface


load_dotenv()  # load .env file

# Get port from environment (GCP Cloud Run uses PORT env var)
PORT = int(os.getenv("PORT", 8000))

OPENAI_Local_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Techline Custom Agent API",
    description="AI-powered cleaning service assistant with address validation",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Techline Custom Agent API is running!"}

@app.post("/chat")
async def chat_with_assistant(request: Request):
    """Send a message to the assistant and get a response (only after address validation)."""
    try:
        thread_id = request.thread_id
        user_message = request.message
        # Add the user's message to the thread
        oa_client.responses.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )
        
        # Create a run with the assistant
        run = oa_client.responses.threads.runs.create(
            thread_id=thread_id,
            assistant_id=oa_client.assistant_id
        )
        
        # Wait for the run to complete
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = oa_client.responses.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status == 'completed':
            # Get the assistant's response
            messages = oa_client.responses.threads.messages.list(thread_id=thread_id)
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


@app.get("/fetch_response")
async def fetch_response(thread_id: str):
    """Fetch the assistant's response for a given thread ID."""
    try:
        messages = oa_client.responses.threads.messages.list(thread_id=thread_id)
        if not messages.data:
            raise HTTPException(status_code=404, detail="No messages found for this thread ID.")
        
        assistant_response = messages.data[0].content[0].text.value
        return {
            "thread_id": thread_id,
            "assistant_response": assistant_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching response: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
