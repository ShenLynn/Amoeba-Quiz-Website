from flask import render_template, flash, redirect, json
from app import app, forms, db
from app.forms import SignupForm
from app.models import User, Attempt

#import testing module
from app.testing import randomQuiz, randomAttempt, PretendGenQuiz, PretendGenAttempt

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
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

#page for testing functionality of 'attempt' table
@app.route('/pretendattempts', methods=['GET','POST'])
def pretend_attempts():
  form1 = PretendGenQuiz()
  form2 = PretendGenAttempt()
  allattempts = Attempt.query.all()
  if form1.validate_on_submit():
    randomQuiz()
  if form2.validate_on_submit():
    randomAttempt()
  return render_template('pretend_attempts.html', form1=form1, form2=form2, attempts=allattempts)

