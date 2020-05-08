from flask import render_template
from app import forms
from app.forms import SignupForm
from app import app

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/index')
def index():
  form = SignupForm()
  return render_template('landingpage.html', form=form)