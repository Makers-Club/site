from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

class User(Base, declarative_base):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)

    def __init__(self, id, email, handle, name=None, avatar_url=None):
        super().__init__()
        self.id = id or str(uuid4())
        self.email = email or str(uuid4())
        self.name = name or handle or str(uuid4())
        self.handle = handle or str(uuid4())
        self.avatar_url = avatar_url
    
    

