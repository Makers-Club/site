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

# DO NOT migrate until all relavent models have been included
class Horse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
