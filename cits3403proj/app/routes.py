from flask import render_template, redirect
from app import forms
from app.forms import SignupForm
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
  form = SignupForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You now have access to quizzes!')
    return redirect('/index')
  return render_template('landingpage.html', form=form)