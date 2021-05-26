from sqlalchemy import Column, String
from models.base import declarative_base, Base

class Session(Base, declarative_base):
    __tablename__ = 'sessions'
    user_id = Column(String(128), nullable=False)
    created_at = Column(String(64), nullable=False)

    def __init__(self, token, user_id):
        super().__init__()
        self.id = token
        self.user_id = user_id
