from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login.user_loader
def load_user(id): #retrieve the user object representing the current user from the database
  return User.query.get(int(id)) #flask-login uses string for ids. database uses integers for id

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, index=True, nullable=False)
  email = db.Column(db.String(120), unique=True, index=True, nullable=False)
  password_hash = db.Column(db.String(128))
  posted_quizes = db.relationship('Quiz', backref = 'postedby', lazy = 'dynamic')
  attempts = db.relationship('Attempt', backref = 'user', lazy = 'dynamic')
  is_admin = db.Column(db.Boolean, default=False, nullable=False)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  #How the object is printed
  def __repr__(self): 
    return f"User('{self.username}', '{self.email}', '{self.is_admin}')"
  
class Quiz(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(32), index=True)
  quizname = db.Column(db.String(32), index=True, unique=True)
  filename = db.Column(db.String(32),unique=True)
  date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  attempts = db.relationship('Attempt', backref = 'quiz', lazy = 'dynamic')

  def __repr__(self): 
    return f"Quiz('{self.quizname}', '{self.category}')"

class Attempt(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
  score = db.Column(db.Integer, index=True)
  date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

  def __repr__(self): 
    return f"Attempt('{self.quiz.quizname}', '{self.user.username}')"
