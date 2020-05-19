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
  return render_template('quiz.html', questionset=questionset)