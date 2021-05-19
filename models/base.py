from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy import Column, String


declarative_base = declarative_base()

class Base():
    id = Column(String(60), nullable=False, primary_key=True)
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        for k, v in kwargs.items():
            self.__dict__[k] = v
        print(self.__dict__, 'yo')
    
    def save(self):
        from models.storage import DB
        DB.save(self)
    
    def delete(self):
        from models.storage import DB
        DB.delete(self)
    
    @classmethod
    def get_by_id(cls, id):
        from models.storage import DB
        return DB.get_by_id(cls, id)
    
    def to_dict(self):
        try:
            del self.__dict__['_sa_instance_state']
        except:
            pass
        return self.__dict__


