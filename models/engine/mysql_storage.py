"""This module creates the db_storage engine"""
from os import getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from models.user import User

# Expected to be a dictionary that associates all known models with its name
models = {'User': User}

class MySQLStorage():
    """This is an instance of the MySQLStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """This creates an instance of the MySQLStorage class"""
        db_credentials = {
            'drivername': 'mysql+pymysql',
            'username': 'root', #getenv('MYSQL_USER'),
            'password': 'root', #getenv('MYSQL_PWD'),
            'database': 'dev_db', #getenv('MYSQL_DB'),
            'host': 'localhost'
        }
        db_url = '{drivername}://{username}:{password}@{host}/{database}'.format(**db_credentials)
        self.__engine = create_engine(db_url, pool_pre_ping=True)

    def all(self, cls=None):
        """Returns all of type cls or all classes if cls=None"""        
        if cls is None:
            objs = []
            for model in models.values():
                objs.extend(self.__session.query(model).all())
        else:
            objs = self.__session.query(models[cls]).all()

        return objs

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """Deletes the object from the current database session"""
        self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        from models.base_model import DBase
    
        DBase.metadata.create_all(self.__engine)
        sf = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session()

    def close(self):
        """Disposes of the current Session, if present"""
        self.__session.close()
    
    def get(self, cls, id):
        """Returns object based on class name and ID or None if not found"""
        
        if type(cls) is str:
            if cls not in models:
                return None
            cls = models[cls]
        elif cls not in models.values():
            return None
        
        return self.__session.query(cls).get(id)
    
    def count(self, cls=None):
        """ Returns count of objects in storage of type cls or
        count of *all* objects if cls is None """
        
        if cls is None:
            return len(self.all())
        
        if type(cls) is str:
            if cls not in models:
                return -1
            cls = models[cls]
        
        if cls not in models.values():
            return -1

        return self.__session.query(cls).count()