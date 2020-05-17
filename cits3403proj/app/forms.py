from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional

class SignupForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
  email = StringField('Email', validators=[Optional(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign Up')

