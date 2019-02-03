from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
	username = db.Column(db.String(32), nullable=False, index=True, unique=True, primary_key=True)
	password_hash = db.Column(db.Text)
	is_admin = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		raise TypeError("cannot read a user's password")

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		if not password:
			return False
		return check_password_hash(self.password_hash, password)
