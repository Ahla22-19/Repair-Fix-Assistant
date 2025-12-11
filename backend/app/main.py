from fastapi import FastAPI
from app.api import auth, chat  # make sure auth.py and chat.py exist

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"status": "ok"}
