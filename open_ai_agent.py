from agents import Agent, Runner , trace
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load .env file

api_key = os.getenv("OPENAI_API_KEY")
oa_client = OpenAI(api_key=api_key)
oa_model = "gpt-4o-mini-2024-07-18"  # Specify the model to use

agent = Agent(name="Cleaning Bot Assistant", instructions="You are a helpful assistant", model=oa_model)

prompt_a = "Hi! Let's get your instant quote. What address will be getting cleaned?"
prompt_b = "We're having trouble locating that address. Retry?"
prompt_c = "We're not in your area yet, but HeyMaid is growing. Would you like to leave your email so we can notify you when we are in your area? We can offer you a percentage discount on your next service once we expand our services in this area"
prompt_d = "Please tell how many rooms, bathrooms and or/area size you need to be cleaned.   "

#wrap this in a class
class AgentWrapper:
    def __init__(self, agent):
        self.agent = agent

    async def make_hardcoded_question(self, prompt_example: str):
        with trace(workflow_name="Hardcoded Question", group_id = "Techline-CustomAgent"):
            new_input = [{"role": "user", "content": prompt_example}]
            result = await Runner.run(self.agent, new_input)
            return result

    async def get_user_question(self, question: str):
        with trace(workflow_name="Conversation", group_id = "Techline-CustomAgent"):
            new_input = [{"role": "user", "content": question}]
            result = await Runner.run(self.agent, new_input)
            return result

    async def answer_question(self, questionResult: str):
        with trace(workflow_name="Answering Question", group_id="Techline-CustomAgent"):
            new_input = [{"role": "assistant", "content": questionResult}]
            result = await Runner.run(self.agent, new_input)
            return result.final_output
    
