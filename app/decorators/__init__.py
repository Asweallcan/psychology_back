from functools import wraps
from flask import make_response
from ..models import User


def login_require(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		response = make_response()
		user = User.get_user_from_cookie()
		if not user:
			response.headers["redirect"] = "login"
			return response
		return f(*args, **kwargs)

	return wrapper


def admin_require(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		response = make_response()
		user = User.get_user_from_cookie()
		if not user.is_admin:
			response.headers["redirect"] = "admin"
			return response
		return f(*args, **kwargs)

	return wrapper
