import os
from fastapi import FastAPI, HTTPException

from dotenv import load_dotenv

from openai import OpenAI
from agents import Agent, Runner


load_dotenv()  # load .env file

api_key = os.getenv("OPENAI_API_KEY")
oa_client = OpenAI(api_key=api_key)
oa_model = "gpt-4o-mini-2024-07-18"  # Specify the model to use

prompt_instructions = "You're a helpful assistant for a cleaning service. Answer questions about cleaning services, schedules, and pricing." \
"\n" \
                      "Your goal is to make the client 4 questions before you can help them with other requests" \
                      "\n" \
                      "Question 1: What is the address for the cleaning service?" \
                      "\n" \
                      "Question 2: What type of cleaning service do you need? (e.g., residential, commercial, deep clean)" \
                      "\n" \
                      "Question 3: How many rooms or areas need cleaning?" \
                      "\n" \
                      
agent = Agent(name="Cleaning Bot Assistant", instructions="You are a helpful assistant", model=oa_model)

#wrap this in a class
class AgentWrapper:
    def __init__(self, agent):
        self.agent = agent

    async def make_hardcoded_question(thread_id, message):
            new_input = [{"role": "user", "content": prompt_instructions}]
            result = await Runner.run(agent,new_input)
            return result


    async def answer_questions(thread_id , message: str):
            new_input = [{"role": "assistant", "content": message}]
            result = await Runner.run(agent, new_input)
            return result.final_output
    