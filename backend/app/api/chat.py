from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User, ChatMessage

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_message(db: Session, user_email: str, role: str, message: str, tokens: int):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return
    chat = ChatMessage(
        user_id=user.id,
        role=role,
        message=message,
        tokens_used=tokens
    )
    user.total_tokens_used += tokens
    db.add(chat)
    db.commit()

# Updated /chat endpoint
@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db), user_email: str = "demo@example.com"):
    """
    Note: replace user_email with real JWT auth in production
    """
    # 1. Save user message
    save_message(db, user_email, "user", request.message, tokens=0)  # tokens=0 for now

    # 2. Get AI response
    response = agent.handle_query(request.message)

    # 3. Count tokens (simplified: 1 token per 4 chars)
    tokens_used = max(1, len(str(response)) // 4)

    # 4. Save assistant message
    save_message(db, user_email, "assistant", str(response), tokens=tokens_used)

    return {"response": response, "tokens_used": tokens_used}
