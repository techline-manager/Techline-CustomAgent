from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file


api_key = os.getenv("OPENAI_API_KEY")
oa_client = OpenAI(api_key=api_key)
oa_model = "gpt-4o-mini-2024-07-18"  # Specify the model to use


prompt_a = "Hi! Let's get your instant quote. What address will be getting cleaned?"
prompt_b = "We're having trouble locating that address. Retry?"
prompt_c = "We're not in your area yet, but HeyMaid is growing. Would you like to leave your email so we can notify you when we are in your area? We can offer you a percentage discount on your next service once we expand our services in this area"
prompt_d = "Please tell how many rooms, bathrooms and or/area size you need to be cleaned.   "


