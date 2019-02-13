from functools import wraps
from flask import make_response
from ..utils import get_user


def login_require(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		response = make_response()
		if not get_user(response):
			return response
		f(*args, **kwargs)

	return wrapper


def admin_require(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		response = make_response()
		user = get_user(response)
		if not user.is_admin:
			response.headers["redirect"] = "admin"
			return response
		f(*args, **kwargs)

	return wrapper
