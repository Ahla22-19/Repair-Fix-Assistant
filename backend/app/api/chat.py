from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.agents.repair_agent import RepairAgent

router = APIRouter()
agent = RepairAgent()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat(request: ChatRequest):
    response = agent.handle_query(request.message)
    return {"response": response}
