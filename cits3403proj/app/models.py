from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, index=True, nullable=False)
  email = db.Column(db.String(120), unique=True, index=True, nullable=False)
  password_hash = db.Column(db.String(128))
  
  #How the object is printed
  def __repr__(self): 
    return f"User('{self.username}', '{self.email}')"