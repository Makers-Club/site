from flask import Flask
from models.storage import DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB_MIGRATION_URI = DB._MySQLClient__engine.url

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_MIGRATION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from models.base import declarative_base, Base
from uuid import uuid4


class User(Base, db.Model):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    handle = Column(String(60), nullable=False)
    avatar_url = Column(String(256), nullable=True)
    id = Column(String(60), nullable=False, primary_key=True)
    credits = Column(Integer)

    def __init__(self, id, email, handle, name=None, avatar_url=None):
        super().__init__()
        self.email = email or str(uuid4())
        self.name = name or handle or str(uuid4())
        self.handle = handle or str(uuid4())
        self.avatar_url = avatar_url
        self.credits = 0


class Session(Base, db.Model):
    __tablename__ = 'sessions'
    user_id = Column(String(128), nullable=False)
    created_at = Column(String(64), nullable=False)
    id = Column(String(60), nullable=False, primary_key=True)

    def __init__(self, token, user_id):
        super().__init__()
        self.id = token
        self.user_id = user_id
