from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from uuid import uuid4
from models.engine import storage


# Used by DBStorage class for loading objects into memory
DBase = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        for x, y in kwargs.items():
            if x in ["created_at", "updated_at"]:
                self.__dict__[x] = datetime.strptime(y, date_format)
            elif x != "__class__":
                self.__dict__[x] = y

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        try:
            del dictionary['_sa_instance_state']
        except:
            pass
        return dictionary

    def delete(self):
        """Delete the current instance from storage by calling delete method"""
        storage.delete(self)