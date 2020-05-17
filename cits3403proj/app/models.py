from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, index=True, nullable=False)
  email = db.Column(db.String(120), unique=True, index=True, nullable=False)
  password_hash = db.Column(db.String(128))
  
  #How the object is printed
  def __repr__(self): 
    return f"User('{self.username}', '{self.email}')"
  
class Quiz(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(32), index=True, unique=True)
  filename = db.Column(db.String(32),unique=True)
  date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Attempt(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
  score = db.Column(db.Integer, index=True)
  date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
