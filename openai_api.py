import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()  # load .env file

oa_Client = OpenAI()

oa_assistant_id = "asst_3JAJtWdX1E9puuIy34vlUDPq"
oa_model = "gpt-4-omini"


# Retrieve the assistant (but don't create a global thread)
oa_agent = oa_Client.responses.assistants.retrieve(oa_assistant_id=oa_assistant_id)

class OpenAI_API():
    def __init__(self, message):
        self.message = message
        self.client = OpenAI()
        self.assistant_id = oa_assistant_id
        self.model = oa_model

