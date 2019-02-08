from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app, request


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
	username = db.Column(db.String(32), nullable=False, index=True, unique=True, primary_key=True)
	email = db.Column(db.String(32), nullable=False)
	password_hash = db.Column(db.Text)
	is_admin = db.Column(db.Boolean, default=False)
	confirmed = db.Column(db.Boolean, default=False)

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

	def generate_confirm_token(self):
		s = Serializer(current_app.config["SECRETE_KEY"], expires_in=60 * 5)
		token = s.dumps({"user": self.username})
		return token.decode()

	@staticmethod
	def verify_confirm_token(token, user):
		s = Serializer(current_app.config["SECRETE_KEY"])
		try:
			data = s.loads(token)
			if user != data["user"]:
				return -1, "Bad signature"
			return 0, "Confirm success"
		except SignatureExpired:
			return -1, "Signature expired"
		except BadSignature:
			return -2, "Bad signature"
