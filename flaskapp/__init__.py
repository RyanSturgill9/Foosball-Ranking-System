from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('flaskapp.config.DevelopmentConfig')

CORS(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
from flaskapp import models
with app.app_context():
    db.create_all()

from flaskapp import routes
