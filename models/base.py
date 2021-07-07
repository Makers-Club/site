from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime



class Base():
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        '''
        Had trouble serializing/deserializing datetimes correctly so
        I'm just getting rid of it for now. Sessions will be ongoing.
        -------------------------------------------------------------
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
            if k == "created_at":
                self.__dict__[k] = datetime.strptime(v, date_format)
        '''
        for k, v in kwargs.items():
            if k != "__class__":
                self.__dict__[k] = v
    
    def to_dict(self):
        dict_repr = self.__dict__
        if 'password' in dict_repr:
            del dict_repr['password']
        return self.__dict__



