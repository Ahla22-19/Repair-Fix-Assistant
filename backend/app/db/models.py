from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # "user" or "assistant"
    message = Column(Text)
    tokens_used = Column(Integer, default=0)

    user = relationship("User", back_populates="messages")

User.messages = relationship("ChatMessage", back_populates="user")
