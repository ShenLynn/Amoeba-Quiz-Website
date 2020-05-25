from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, Length, Optional

class SignupForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
  email = StringField('Email', validators=[Optional(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submitSignup = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submitLogin = SubmitField('Log in')

class DeleteQuizForm(FlaskForm):
  submitDelete = SubmitField('Delete quiz')

class DeleteUserForm(FlaskForm):
  submitDelete = SubmitField('Delete user')

class AddQuizForm(FlaskForm):
  quizname = StringField('Quizname', validators=[DataRequired(), Length(min=1, max=20)])
  category = StringField('Category', validators=[DataRequired(), Length(min=1, max=20)])
  quiz = FileField('Document', validators=[FileRequired(), FileAllowed(['json'], 'Only JSON documents!')])
  submitQuiz = SubmitField('Submit Quiz')

class SubmitQuizResults(FlaskForm):
  submitResults = SubmitField('Submit Results')