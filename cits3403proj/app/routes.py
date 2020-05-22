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

@app.route('/login', methods=['POST', 'GET'])
def signup_login():
  form = SignupForm()
  return render_template('signuplogin_page.html', form=form)

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():

  questionset = {
    "questions":[
    {
    "question": "Which of these is a virus?",
      "answers":[
        "Staphylococcus",
        "leukemia",
        "Scoliosis",
        "chicken pox"
      ],
    "answerindex": 3
    },
    {
    "question": "Among these elements, which one has the highest atomic mass?",
      "answers":[
        "Helium",
        "Sodium",
        "Uranium",
        "Copper"
      ],
    "answerindex": 2
    },
    {
    "question": " Which of these has the longest wave length?",
      "answers":[
        "Radio waves",
        "Visible light",
        "X-rays",
      ],
    "answerindex": 0
    },
  ]
  }
<<<<<<< HEAD
  return render_template('quiz.html', questionset=questionset)
=======
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

>>>>>>> bc8612f950db416e1b4de317d64c1095bdda175d
