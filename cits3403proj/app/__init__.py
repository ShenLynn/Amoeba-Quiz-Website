from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
<<<<<<< HEAD
from flask_login import LoginManager
=======
>>>>>>> signup_form

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #Creates database object
migrate = Migrate(app, db)
<<<<<<< HEAD
login = LoginManager(app)
=======
>>>>>>> signup_form

from app import routes, models


