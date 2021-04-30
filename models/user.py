from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import DBase, BaseModel

class User(BaseModel, DBase):
    """ User model """
    ___tablename__ = 'users'
    email = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)