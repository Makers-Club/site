from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base

class User(Base, declarative_base):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)

    def __init__(self, id, email, name, handle, avatar_url=None):
        super().__init__()
        self.id = id # Users will use Github IDs rather than our own uuid's
        self.email = email
        self.name = name
        self.handle = handle
        self.avatar_url = avatar_url

    

