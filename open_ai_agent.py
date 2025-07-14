import os
from fastapi import FastAPI, HTTPException


from openai import OpenAI
import openai as openai_api

from dotenv import load_dotenv

load_dotenv()  # load .env file

oa_model = "gpt-4o-mini-2024-07-18"  # Specify the model to use
ASSISTANT_ID = "asst_3JAJtWdX1E9puuTy34v1UDPq"
                
def get_openai_response(messages):
    """
    Send the conversation to the Assistant API and get the assistant's reply.
    """
    thread = openai_api.responses.create(messages=messages)
    run = openai_api.responses.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    # Wait until run completes (blocking)
    import time
    while True:
        run_status = openai_api.responses.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status in ["completed", "failed"]:
            break
        time.sleep(0.5)
    
    if run_status.status == "completed":
        messages_out = openai_api.responses.list(thread_id=thread.id)
        # Last message should be the assistant's
        for m in reversed(messages_out.data):
            if m.role == "assistant":
                return m.content[0].text.value
    return "[No reply]"