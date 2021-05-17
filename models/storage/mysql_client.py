from os import getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base import declarative_base



class MySQLClient():
    def __init__(self, credentials):
        self.__engine = create_engine(URL(**credentials), pool_pre_ping=True)
    
    def reload(self):
        declarative_base.metadata.create_all(self.__engine)
        sf = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session()

    def is_connected(self):
        return True if self.__engine else False
    
    def save_obj_to_db(self, obj):
        self.__session.add(obj)
        self.__session.commit()
    
    def get_from_db_by_id(self, cls: type, id: str):
        return self.__session.query(cls).filter_by(id=id).one()



