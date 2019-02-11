from . import api
from flask import request
from flask_mail import Message
from ..models import User
from ..utils import get_user, response_with_status, make_response
from ..db import db
from ..mail import mail


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
	if not user:
		response = response_with_status(-1, "username does not exists")
		response.set_cookie("user", None)
		return response
	if not user.verify_password(data["password"]):
		response = response_with_status(-1, "password wrong")
		response.set_cookie("user", None)
		return response
	if not user.confirmed:
		response = response_with_status(-2, "need confirmation")
		token = user.generate_confirm_token()
		send_confirm(path=data["path"], token=token, username=user.username, forget=False, recipients=[user.email, ])
		response.set_cookie("user", user.username, max_age=60 * 5 + 1)
		return response
	response = response_with_status(0, "login success", user.to_json())
	response.set_cookie("user", user.username, max_age=(60 * 60 * 24 * 7) if data["remember"] else 0)
	return response


@api.route("/register", methods=["POST"])
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
		return "", 500
	send_confirm(path=data["path"], username=data["username"], forget=False, token=token, recipients=[data["email"], ])
	response = response_with_status(0, "Register success")
	response.set_cookie("user", data["username"], max_age=5 * 60 + 1, httponly=True)
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
	username = request.cookies.get("user")
	status, statusText = User.verify_confirm_token(data["token"].encode(), username)
	if status == 0 and not data["forget"]:
		user = User.query.filter_by(username=username).first()
		user.confirmed = True
		try:
			db.session.add(user)
			db.session.commit()
		except:
			db.session.rollback()
			return "", 500
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
	send_confirm(path=path, token=token, forget=data["forget"], username=user.username, recipients=[user.email, ])
	response = response_with_status(0, "Send success")
	response.set_cookie("user", user.username, max_age=5 * 60 + 1)
	return response


@api.route("/change_user_fields", methods=["POST"])
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
	user = User.query.filter_by(username=data["user"]).first() or get_user(response)
	if not user:
		if not data["user"]:
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
		return "", 500
	return response_with_status(0, "change success")


def send_confirm(path, token, username, forget: bool, recipients: list):
	"""
	:param path: 目标系统的url地址
	:param token: 邮箱验证token
	:param username: 用户名
	:param forget: 是否是忘记密码的邮件
	:param recipients: 接收人
	"""
	message = Message(subject="心理评测系统邮箱激活", recipients=[*recipients, ])
	if not forget:
		message.html = """
			<h2>你好，{username}</h2>
			<p>欢迎你使用吕世豪的心理评测系统，请点击下面的连接激活你的账号。</p>
			<p><a href="{path}/confirm?token={token}&user={username}">{path}/confirm?token={token}&user={username}</a></p>
			""".format(username=username, path=path, token=token)
	else:
		message.html = """
			<h2>你好，{username}</h2>
			<p>请点击下面的按钮进行密码修改。</p>
			<p><a href="{path}/confirm?token={token}&user={username}&forget={forget}">{path}/confirm?token={token}&user={username}&forget={forget}</a></p>
			""".format(username=username, path=path, token=token, forget=int(forget))
	mail.send(message)
