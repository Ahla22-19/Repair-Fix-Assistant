from fastapi import FastAPI
from app.api import auth, chat

app = FastAPI(title="Repair Fix Assistant API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def health_check():
    return {"status": "ok"}
