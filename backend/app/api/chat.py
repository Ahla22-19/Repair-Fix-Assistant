from fastapi import APIRouter

router = APIRouter()

# Example endpoint
@router.get("/ping")
async def ping():
    return {"message": "pong"}
