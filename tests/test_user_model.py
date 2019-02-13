import unittest
from app.models import User

user = User(username="lvshihao", password="123456")


class TestUser(unittest.TestCase):

	def test_get_password(self):
		with self.assertRaises(TypeError):
			password = user.password

	def test_password_hash(self):
		self.assertTrue(user.verify_password("123456"))
		self.assertFalse(user.verify_password("321564"))
