from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import DBase, BaseModel

class User(BaseModel, DBase):
    """ User model """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    username = Column(String(60), nullable=False)
    profile_pic = Column(String(256), nullable=True)

