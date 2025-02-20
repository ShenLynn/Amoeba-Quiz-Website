from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #Creates database object
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'signup_login'

from app import routes, models, admin, errors


