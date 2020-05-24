from flask import render_template, flash, redirect, url_for, request, json
from app import app, forms, db
from app.forms import SignupForm, LoginForm
from app.models import User, Attempt, Quiz
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import distinct

#import testing module
from app.testing import randomQuiz, randomAttempt, PretendGenQuiz, PretendGenAttempt

@app.route('/')
@app.route('/index')
def index():
  return render_template('landingpage.html')

@app.route('/login', methods=['GET', 'POST'])
def signup_login():
  if current_user.is_authenticated: #do not show the signup/login page to users who are already logged in
    return redirect(url_for('index'))
  form1 = SignupForm()
  form2 = LoginForm()

  #if user submits signup form
  if form1.submitSignup.data and form1.validate_on_submit():
    user = User(username=form1.username.data, email=form1.email.data)
    user.set_password(form1.password.data) #store hash of user's password
    db.session.add(user)
    db.session.commit()
    flash('Thanks for signing up, you can now log in')
    return redirect(url_for('signup_login'))
  
  #if user submits login form
  if form2.submitLogin.data and form2.validate_on_submit():
    user = User.query.filter_by(username=form2.username.data).first()

    #if provided username doesnt exist or incorrect password
    if user is None or not user.check_password(form2.password.data):
      flash('Invalid username or password')
      return redirect(url_for('signup_login'))
    
    #else login successful
    login_user(user) #store the logged in user in current_user
    next_page = request.args.get('next') #send user to their intended page, if they were redirected due to not logged in
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page) #return user to whatever page they were visiting, but now logged in
  return render_template('signuplogin_page.html', signForm=form1, logForm=form2)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

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

#quiz categories page
@app.route('/categories', methods=['GET', 'POST'])
def categories():
  #retrieve distinct list of categories available
  catlist = [cat[0] for cat in db.session.query(distinct(Quiz.category))]
  #dictionary to map category to list of its quizes
  quizdic = {}
  for category in catlist:
    quizdic[category] = Quiz.query.filter_by(category=category).all()

  return render_template('categories.html', catlist=catlist, quizdic=quizdic)

#page for testing functionality of 'attempt' table
@app.route('/pretendattempts', methods=['GET','POST'])
def pretend_attempts():
  form1 = PretendGenQuiz()
  form2 = PretendGenAttempt()
  allattempts = Attempt.query.all()
  if form1.submitQuiz.data and form1.validate_on_submit():
    randomQuiz()
  elif form2.submitAttempt.data and form2.validate_on_submit():
    randomAttempt()
  return render_template('pretend_attempts.html', form1=form1, form2=form2, attempts=allattempts)

@app.route('/personal')
def personal():
  return render_template('personal.html')

