from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import hash_password, verify_password, create_access_token
from pydantic import BaseModel
router = APIRouter()


class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    email = request.email
    password = request.password

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        email=email,
        hashed_password=hash_password(password)  # make sure User model has `hashed_password`
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    email = request.email
    password = request.password
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}
