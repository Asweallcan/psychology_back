from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app
from datetime import datetime


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
	username = db.Column(db.String(32), nullable=False, index=True, unique=True, primary_key=True)
	email = db.Column(db.String(32), nullable=False)
	password_hash = db.Column(db.Text)
	is_admin = db.Column(db.Boolean, default=False)
	last_seen = db.Column(db.DateTime, default=datetime.now)
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
	def verify_confirm_token(token, username):
		s = Serializer(current_app.config["SECRETE_KEY"])
		user = User.query.filter_by(username=username).first()
		if not user:
			return -2, "Bad signature"
		try:
			data = s.loads(token)
			if username != data["user"]:
				return -2, "Bad signature"
			return 0, "Confirm success"
		except SignatureExpired:
			return -1, "Signature expired"
		except BadSignature:
			return -2, "Bad signature"

	def to_json(self):
		return {
			"username": self.username,
			"email": self.email,
			"is_admin": self.is_admin,
			"last_seen": self.last_seen
		}

	def update_last_seen(self):
		self.last_seen = datetime.now()
		db.session.add(self)
		db.session.commit()
