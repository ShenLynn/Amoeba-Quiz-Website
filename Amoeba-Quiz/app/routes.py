from flask import render_template, flash, redirect, url_for, request, json
from app import app, forms, db
from app.forms import SignupForm, LoginForm, DeleteQuizForm, AddQuizForm, DeleteUserForm
from app.models import User, Attempt, Quiz
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from sqlalchemy import distinct
from sqlalchemy.sql import func
import os

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
  return redirect(url_for('signup_login'))

@app.route('/quiz/<quizid>', methods=['POST', 'GET'])
@login_required
def quiz(quizid):
  quiz = Quiz.query.filter_by(id=quizid).first()
  filename = quiz.filename
  basedir = os.path.abspath(os.path.dirname(__file__))
  quiz_dir = os.path.join(basedir, 'static', 'quizzes')
  file_dir = os.path.join(quiz_dir, filename)
  with open(file_dir) as json_file:
    questionset = json.load(json_file)
  return render_template('quiz.html', questionset=questionset, quizname=quiz.quizname, quizcat=quiz.category, quizid=quizid)

@app.route('/results/<quizid>/<score>', methods=['POST', 'GET'])
@login_required
def results(quizid, score):
  attempt = Attempt(user_id = current_user.id, score=score, quiz_id=quizid)
  db.session.add(attempt)
  db.session.commit()
  return redirect(url_for('profile', username=current_user.username) )

#quiz categories page
@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
  #retrieve distinct list of categories available
  catlist = [cat[0] for cat in db.session.query(distinct(Quiz.category)).order_by(Quiz.category)]
  #dictionary to map category to list of its quizes
  quizdic = {}
  for category in catlist:
    quizdic[category] = Quiz.query.filter_by(category=category).all()

  return render_template('categories.html', catlist=catlist, quizdic=quizdic)

#admin view that allows them to delete quizes
@app.route('/deletequiz/<quizid>', methods=['GET','POST'])
@login_required
def deletequiz(quizid):
  if(current_user.is_admin==False):
    return redirect(url_for('index')) #do not allow non-admin users to visit this page.
  quiz = Quiz.query.filter_by(id=quizid).first()
  delquizform = DeleteQuizForm()
  confirmed = False
  if delquizform.submitDelete.data and delquizform.validate_on_submit():
    db.session.delete(quiz)
    db.session.commit()
    confirmed = True
  return render_template('delete_quiz.html', quiz=quiz, delquizform=delquizform, confirmed=confirmed)

@app.route('/user/<username>')
@login_required
def profile(username):
  user = User.query.filter_by(username=username).first_or_404()
  joindate = user.date_joined.strftime("%d %b %Y")
  favcats = []
  favcatsplays = []
  hiquizzes = []
  hiscores = []
  totalattempts = 0
  totalscore = 0
  madeattempt = Attempt.query.filter_by(user_id = user.id).first() is not None
  datadic = {}
  if madeattempt:
    #find favourite categories and number of plays in that category. Add at most 4 to correspoinding lists.
    categoryranking = db.session.query(Attempt, Quiz, func.count(Quiz.category)).filter(Attempt.quiz_id==Quiz.id, Attempt.user_id==user.id).group_by(Quiz.category).order_by(func.count(Quiz.category).desc()).limit(4).all()
    for i in range(0, len(categoryranking)):
      favcats.append(categoryranking[i][1].category)
      favcatsplays.append(categoryranking[i][2])
    
    #find highscores and the quiz it was achieved in
    scoreranking = db.session.query(Attempt, Quiz, func.max(Attempt.score)).filter(Attempt.quiz_id==Quiz.id, Attempt.user_id==user.id).group_by(Quiz.id).order_by(func.max(Attempt.score).desc()).limit(4).all()
    for i in range(0, len(scoreranking)):
      hiquizzes.append(scoreranking[i][1].quizname)
      hiscores.append(scoreranking[i][2])
    
    #find user's total number of quiz plays
    allplays = db.session.query(func.count(Attempt.user_id)).filter_by(user_id=user.id).first()
    totalattempts = allplays[0]

    #find user's total score
    allscores = db.session.query(func.sum(Attempt.score)).filter_by(user_id=user.id).first()
    totalscore = allscores[0]
  
  #add all data to a dictionary for jinja
  datadic["joindate"]=joindate
  datadic["favcats"]=favcats
  datadic["favcatlen"]=len(favcats)
  datadic["favcatsplays"]=favcatsplays
  datadic["hiquizzes"]=hiquizzes
  datadic["hiquizlen"]=len(hiquizzes)
  datadic["hiscores"]=hiscores
  datadic["totalattempts"]=totalattempts
  datadic["totalscore"]=totalscore
  datadic["madeattempt"]=madeattempt

  return render_template("profile.html", user=user, datadic=datadic)

@app.route('/customizeamoeba')
@login_required
def customamoeba():
  return render_template("customize_amoeba.html")

@app.route('/leaderboards')
@login_required
def leaderboards():
  #scores across any category, any quiz
  lb_all = db.session.query(User,Quiz,Attempt).filter(Attempt.user_id==User.id, Attempt.quiz_id==Quiz.id).order_by(Attempt.score.desc()).all()

  #dictionary mapping scores across a given category name
  lb_cat = {}
  #dictionary mapping scores across a give quiz name
  lb_quiz = {}

  #retrieve distinct list of categories available
  catlist = [cat[0] for cat in db.session.query(distinct(Quiz.category)).order_by(Quiz.category)]
  #dictionary to map category to list of its quizes
  quizdic = {}
  for category in catlist:
    quizdic[category] = Quiz.query.filter_by(category=category).all()
    lb_cat[category] = db.session.query(User,Quiz,Attempt).filter(Attempt.user_id==User.id, Attempt.quiz_id==Quiz.id, Quiz.category==category).order_by(Attempt.score.desc()).all()
    for quiz in quizdic[category]:
      lb_quiz[quiz.quizname] = db.session.query(User,Quiz,Attempt).filter(Attempt.user_id==User.id, Attempt.quiz_id==Quiz.id, Quiz.quizname==quiz.quizname).order_by(Attempt.score.desc()).all()
  
  datadic={}
  datadic["catlist"]=catlist
  datadic["quizdic"]=quizdic
  datadic["lb_all"]=lb_all
  datadic["lb_cat"]=lb_cat
  datadic["lb_quiz"]=lb_quiz

  return render_template("leaderboards.html", datadic=datadic)
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

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if(current_user.is_admin==False):
    return redirect(url_for('index')) #only admins can visit this page
  quizform=AddQuizForm()
  if quizform.validate_on_submit():
    basedir = os.path.abspath(os.path.dirname(__file__))
    quiz_dir = os.path.join(basedir, 'static')
    quizfile = quizform.quiz.data

    quizfilename = secure_filename(quizfile.filename)
    # save the quiz file
    quizfile.save(os.path.join(quiz_dir, 'quizzes', quizfilename))

    flash('Quiz uploaded successfully.')
    quiz = Quiz(quizname=quizform.quizname.data, category=quizform.category.data, filename=quizfilename, user_id=current_user.id )
    db.session.add(quiz)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('uploadquestions.html', quizform=quizform)

@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
  if(current_user.is_admin==False):
    return redirect(url_for('index')) #only admins can visit this page
  users = User.query.all()
  return render_template('usersview.html', users=users)

@app.route('/deleteuser/<userid>', methods=['GET','POST'])
@login_required
def deleteuser(userid):
  if(current_user.is_admin==False):
    return redirect(url_for('index')) #only admins can visit this page
  user = User.query.filter_by(id=userid).first_or_404()
  deluserform = DeleteUserForm()
  confirmed = False

  if deluserform.submitDeleteUser.data and deluserform.validate_on_submit():
    confirmed = True
    #delete all quiz attempt data associated with the user
    for attempt in user.attempts:
      db.session.delete(attempt)
      db.session.commit()
    db.session.delete(user)
    db.session.commit()
  return render_template('delete_user.html', user=user, deluserform=deluserform, confirmed=confirmed)

@app.route('/administration', methods=['GET','POST'])
@login_required
def administration():
  if(current_user.is_admin==False):
    return redirect(url_for('index')) #only admins can visit this page
  return render_template('administration.html')
