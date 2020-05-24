from flask import Flask
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from app import app, db
from app.models import User, Attempt, Quiz

admin= Admin(app, name='microblog')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Attempt, db.session))
admin.add_view(ModelView(Quiz, db.session))


