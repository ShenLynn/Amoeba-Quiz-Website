import unittest
from app import app, db
from app.models import User, Quiz, Attempt

class UserModelCase(unittest.TestCase):
  def setUp(self):
    app.config.from_object('config.TestConfig')
    self.app=app.test_client()
    db.create_all()
    u1 = User(id=1, username='amoe', email='amoe@gmail.com')
    u2 = User(id=2, username='susan', email='susan@gmail.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_password_hashing(self):
    u = User(username='Amoeba')
    u.set_password('Squishy')
    self.assertFalse(u.check_password('crunchy'))
    self.assertTrue(u.check_password('Squishy'))

  #test that users can post quizzes and get added to the quiz table
  def test_user_posted_quiz(self):
    u = User(username="Amoeba", email='amoeba@squishy.com')
    quiz = Quiz(category="Animals", filename="otters.json", user_id=u.id)
    self.assertEqual(quiz.postedby.username,u.id)
  
  def test_user_attempt_quiz(self):
    u = User(username="susan", email='susans@gmail.com')
    quiz = Quiz(category="Movies", filename="otters.json", user_id=1)
    attempt = Attempt(user_id=u.id, quiz_id=quiz.id, score=5)
    self.assertEqual(attempt.user.id,u.id)

if __name__ == '__main__':
  unittest.main(verbosity=2)

 


""" 
  #def test_profile(self):

  #test that users can post quizzes and get added to the quiz table
  def test_user_posted_quiz(self):
    u = User(username="Amoeba", email='amoeba@squishy.com')
    quiz = Quiz(category="Animals", filename="otters.json", user_id=u.id)
    self.assertTrue(quiz.postedby.id=u.id)
  
  def test_user_attempt_quiz(self):
    u = User(username="susan", email='susans@gmail.com')
    quiz = Quiz(category="Movies", filename="otters.json", user_id=1)
    attempt = Attempt(user_id=u.id, quiz_id=quiz.id, score=5)
    self.assertTrue(attempt.user.id=u.id)

  #admin tests
  #def test_delete_user(self):
  #def test_delete_quiz

Class TestViews(TestBase):
  def test_homepage_view(self):
    response = self.client


    



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

""" 


  