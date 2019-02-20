from . import api
from flask import request, current_app
from ..models import User
from ..utils import send_confirm, response_with_status, make_response, error_response
from ..db import db
from ..decorators import login_require
import traceback


@api.route("/user", methods=["POST", "GET", "PUT", "DELETE"])
def user():
	if request.method == "POST":
		return register()
	elif request.method == "GET":
		return user_info()
	elif request.method == "PUT":
		return change_user_fields()
	elif request.method == "DELETE":
		return delete_user()


@api.route("/login", methods=["POST"])
def login():
	"""
	登陆接口参数:
		username: 用户名或者邮箱
		password: 密码
		remember: 是否记住用户，提供cookie记录用户
		path: 如果没有验证，需要提供目标系统的origin
	返回参数:
		status: -1 用户名或者密码错误 / -2 用户邮箱未通过验证 / 0 登陆成功
		statusText:
		data:
	"""
	data = request.json
	user = User.query.filter(User.username == data["username"]).first()
	if not user or not user.verify_password(data["password"]):
		response = response_with_status(-1, "username or password wrong")
		User.delete_user_cookie(response)
		return response
	if not user.confirmed:
		response = response_with_status(-2, "need confirmation")
		token = user.generate_confirm_token()
		send_confirm(path=data["path"], token=token, username=user.username, forget=False, recipients=[user.email, ],
		             sender=current_app.config["MAIL_DEFAULT_SENDER"])
		User.set_user_cookie(user, response, confirm=True)
		return response
	response = response_with_status(0, "login success")
	User.set_user_cookie(user, response, remember=data["remember"])
	return response


@api.route("/confirm", methods=["POST"])
def confirm():
	"""
	邮箱验证接口参数:
		token: 邮箱验证token
	返回参数:
	status: -1 token过期 / -2 token错误 / 0验证成功
	statusText:
	data:
	"""
	data = request.json
	user = User.get_user_from_cookie()
	if not user:
		return response_with_status(-2, "Bad signature")
	status, statusText = User.verify_confirm_token(data["token"].encode(), user.username)
	if status == 0 and not data["forget"]:
		user = User.query.filter_by(username=user.username).first()
		user.confirmed = True
		try:
			db.session.add(user)
			db.session.commit()
		except:
			db.session.rollback()
			traceback.print_exc()
			return error_response()
	return response_with_status(status, statusText)


@api.route("/send_confirm", methods=["POST"])
def re_send_confirm():
	"""
	重新发送验证接口参数:
		forget: 是否是忘记密码
		path: 目标系统页面的origin，拼接邮箱中的链接
		user: 验证的用户名
	返回参数:
		status: -1 用户名错误，找不到用户 / 0 验证成功 / 1 已经验证过，非忘记密码的时候使用
		statusText:
		data:
	"""
	data = request.json
	path = data["path"]
	user = User.query.filter_by(username=data["user"]).first()
	if not user:
		return response_with_status(-1, "Can not find user")
	if user.confirmed and not data["forget"]:
		return response_with_status(1, "Confirm already")
	token = user.generate_confirm_token()
	send_confirm(path=path, token=token, forget=data["forget"], username=user.username, recipients=[user.email, ],
	             sender=current_app.config["MAIL_DEFAULT_SENDER"])
	response = response_with_status(0, "Send success")
	User.set_user_cookie(user, response, confirm=True)
	return response


@api.route("/logout", methods=["POST"])
def logout():
	"""
	退出登录接口参数：
		无
	返回参数:
		status: 0 退出成功
		statusText
		data
	"""
	user = User.get_user_from_cookie()
	if user:
		user.update_last_seen()
	response = response_with_status(0, "logout success")
	User.delete_user_cookie(response)
	return response


@login_require
def user_info():
	"""
	获取用户数据接口参数：
		无
	返回参数:
		status: 0 返回成功
		statusText
		data: { username, is_admin, email, last_seen }
	"""
	user = User.get_user_from_cookie()
	return response_with_status(0, "Success", user.to_json())


def register():
	"""
	注册接口参数:
		username: 用户名
		password: 密码
		email: 邮箱
		path: 目标系统的origin
	返回参数:
		status: -1 用户或者账号已经存在 / 0 注册成功
		statusText:
		data:
	"""
	data = request.json
	if User.query.filter_by(username=data["username"]).first() is not None:
		return response_with_status(-1, "Username already exists")
	user = User(username=data["username"], email=data["email"], password=data["password"])
	token = user.generate_confirm_token()
	try:
		db.session.add(user)
		db.session.commit()
	except:
		db.session.rollback()
		traceback.print_exc()
		return error_response()
	send_confirm(path=data["path"], username=data["username"], forget=False, token=token, recipients=[data["email"], ],
	             sender=current_app.config["MAIL_DEFAULT_SENDER"])
	response = response_with_status(0, "Register success")
	User.set_user_cookie(user, response, confirm=True)
	return response


def change_user_fields():
	"""
	重新发送验证接口参数:
		fields: 需要修改数值的参数列表
		values: 对应上面的参数值
		user: 用户名
	返回参数:
		status: -1 找不到用户名 / 0 修改成功
		statusText:
		data:
	"""
	data = request.json
	response = make_response()
	user = User.query.filter_by(username=data["user"]).first() or User.get_user_from_cookie()
	if not user:
		if not data["user"]:
			response.headers["redirect"] = "login"
			return response
		else:
			return response_with_status(-1, "can not find user")
	for i in range(len(data["fields"])):
		setattr(user, data["fields"][i], data["values"][i])
	try:
		db.session.add(user)
		db.session.commit()
	except:
		db.session.rollback()
		traceback.print_exc()
		return error_response()
	return response_with_status(0, "change success")


def delete_user():
	pass
