from sqlalchemy import Column, String, Float, Text
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4

class Charge(Base, declarative_base):
    __tablename__ = 'charge'
    json = Column(Text(32765), nullable=False)
    

    def __init__(self, json):
        super().__init__()
        self.json = json
    
    
