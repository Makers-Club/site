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

    def __init__(self, *args, **kwargs):

        super().__init__()
        self.id = kwargs['id'] # Users will use Github IDs rather than our own uuid's
        self.email = kwargs['email']
        self.username = kwargs['login']
        self.profile_pic = kwargs['avatar_url']

        # Fill name fields safely
        name_list = kwargs['name'].split()
        self.first_name = name_list[0]
        self.last_name = ' '.join(name_list[1:])
        del name_list

    

