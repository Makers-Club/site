"""This module creates the db_storage engine"""
from os import getenv
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from models.user import User

# Expected to be a dictionary that associates all known models with its name
models = {'User': User}

db_credentials = {
    'drivername': 'mysql+pymysql',
    'username': 'root',  # getenv('MYSQL_USER'),
    'password': '123123',  # getenv('MYSQL_PWD'),
    'database': 'dev_db',  # getenv('MYSQL_DB'),
    'host': 'localhost',
    'query': None
}

db_socket_dir = '/cloudsql'  # getenv('DB_SOCKET_DIR')
db_connection_name = 'maker-teams-site:us-central1:mt-mysql-db' # getenv('DB_CONNECTION_NAME')

if getenv('DB_ENV_TYPE') == 'production':
    db_credentials['database'] = 'prod_db'
    db_credentials['host'] = ''
    db_credentials['query'] = {
        'unix_socket': '{}/{}'.format(db_socket_dir, db_connection_name)
    }


class MySQLStorage():
    """This is an instance of the MySQLStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """This creates an instance of the MySQLStorage class"""
        self.__engine = create_engine(URL(**db_credentials), pool_pre_ping=True)

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