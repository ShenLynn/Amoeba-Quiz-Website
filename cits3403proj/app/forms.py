from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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