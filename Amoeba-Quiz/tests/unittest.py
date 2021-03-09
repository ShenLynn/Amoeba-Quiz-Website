import unittest
from app import app, db
from app.models import User, Quiz, Attempt

class TestBase(unittest.TestCase):
  def setUp(self):
    app.config.from_object('config.TestConfig')
    self.app=app.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestModels(TestBase):
  def test_password_hashing(self):
    u = User(username='Amoeba')
    u.set_password('Squishy')
    self.assertFalse(u.check_password('crunchy'))
    self.assertTrue(u.check_password('Squishy'))

  #test that users can post quizzes and get added to the quiz table
  def test_user_posted_quiz(self):
    u = User(username="Amoeba", email='amoeba@squishy.com', id=1)
    quiz = Quiz(category="Animals", filename="otters.json", user_id=u.id)
    db.session.add(quiz)
    db.session.commit()
    q = quiz.query.filter_by(filename="otters.json").first().postedby.id
    self.assertEqual(q,u.id)

  def test_user_attempt_quiz(self):
    u = User(username="susan", email='susans@gmail.com', id=1)
    quiz = Quiz(category="Movies", filename="otters.json", user_id=u.id)
    attempt = Attempt(user_id=u.id, quiz_id=quiz.id, score=5)
    self.assertEqual(attempt.user_id,u.id)

'''  
  def test_delete_user(self):
    
  def test_delete_quiz(self):

class TestRoutes(TestBase):
  def test_home_route(self):

  def test_login_route(self):
  
  def test_profile_route(self):
    #test that profile is visible only after login
  
  def test_admin_route(self):
    #test that admin page is only visible after login + user is admin
  
  def test_quiz_route(self):
    #test that quiz category and quiz is only visible after user login

class TestErrorPages(TestBase):
  def test_404(self):
    response = self.client.get('/doesnotexist')
    self.assertEqual(response.status_code, 404)
    self.assertTrue("404" in response.data)
'''

if __name__ == '__main__':
  unittest.main(verbosity=2)

 
