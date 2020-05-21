#file to declare classes/functions used for testing only
import random, string
from app import app, db
from app.models import User, Attempt, Quiz
from flask_wtf import FlaskForm
from wtforms import SubmitField

#function to generate a random quiz entry in quiz table, using an existing user.
#category = random, 5-15 character string
def randomQuiz():
    nameLength = random.randint(5,15)
    quizname = ""
    for i in range(0,nameLength):
      quizname += random.choice(string.ascii_letters)
    quizfilename = quizname + '.JSON'
    randuser = random.choice(User.query.all())
    quiz = Quiz(category=quizname, filename=quizfilename, user_id=randuser.id)
    db.session.add(quiz)
    db.session.commit()

#function to generate a random attempt entry in the attempt table, using an existing user and quiz
def randomAttempt():
  randuser = random.choice(User.query.all())
  randquiz = random.choice(Quiz.query.all())

  #do not attempt to add entries to the attempt table, if either no users or no quizes exist yet
  if not (randuser and randquiz):
    return
  randscore = random.randrange(0, 10000, 500)

  attempt = Attempt(user_id=randuser.id, quiz_id=randquiz.id, score=randscore)
  db.session.add(attempt)
  db.session.commit()

class PretendGenAttempt(FlaskForm):
  submit = SubmitField('Generate random user attempt')

class PretendGenQuiz(FlaskForm):
  submit = SubmitField('Generate a random quiz')