from flask import render_template, redirect, json
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

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():

  questionset = {
    "questions":[
    {
    "question": "What is your name?",
      "answers":[
        "Shen",
        "lawrence",
        "mary",
        "peter"
      ],
    "answerindex": 0
    },
    {
    "question": "Favourite colour?",
      "answers":[
        "Red",
        "yellow",
        "purple",
        "bob"
      ],
    "answerindex": 3
    },
    {
    "question": "3+4",
      "answers":[
        "1",
        "7",
        "9",
        "0"
      ],
    "answerindex": 1
    },
  ]
  }
  return render_template('quiz.html', questionset=questionset)