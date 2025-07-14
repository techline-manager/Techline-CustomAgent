from fastapi import APIRouter
from open_ai_agent import AgentWrapper

router = APIRouter()




@router.get("/chat_answer")
async def get_chat_answer(request: dict):
    data = request.get("data", {})
    thread_id = data.get("thread_id")
    message = data.get("message")
    result = AgentWrapper.answer_questions(thread_id, message)
    return result



@router.post("/start_conversation")
async def start_conversation(request: dict):
    data = request.get("data", {})
    thread_id = data.get("thread_id")
    message = data.get("message")
    result = AgentWrapper.make_hardcoded_question(thread_id, message)
    return result

@router.post("/chat")
async def chat_with_assistant(request: dict):
    data = request.get("data", {})
    thread_id = data.get("thread_id")
    message = data.get("message")
    result = AgentWrapper.chat_with_assistant(thread_id, message)
    return result

