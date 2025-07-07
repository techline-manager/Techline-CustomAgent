from openai import OpenAI

oa_Client = OpenAI()

oa_assistant_id = "asst_3JAJtWdX1E9puuIy34vlUDPq"
oa_model = "gpt-4-omini"


# Retrieve the assistant (but don't create a global thread)
oa_agent = oa_Client.responses.assistants.retrieve(oa_assistant_id=oa_assistant_id)

