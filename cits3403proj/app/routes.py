from flask import render_template, redirect, json
from app import forms
from app.forms import SignupForm, QuizForm
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
  form = QuizForm()

  questionset = {
    "questions":[
    {
    "question": "What is your name?",
      "answers":[
        "Shen",
        "lawrence",
        "mary",
        "bob"
      ],
    "answerindex": 0
    },
    {
    "question": "Favourite colour?",
      "answers":[
        "Red",
        "blue",
        "purple",
        "bob"
      ],
    "answerindex": 4
    },
  ]
  }
  return render_template('quiz.html', form=form, questionset=questionset)