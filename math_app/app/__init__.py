from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

with app.app_context():
    db.Model.metadata.reflect(db.engine)

from app import routes, models