from . import api
from flask import request
from flask_mail import Message
from ..models import User
from ..utils import response_with_status
from ..db import db
from ..mail import mail


@api.route("/register", methods=["POST"])
def register():
	data = request.json
	if User.query.filter_by(username=data["username"]).first() is not None:
		return response_with_status(-1, "Username already exists")
	user = User(username=data["username"], email=data["email"], password=data["password"])
	token = user.generate_confirm_token()
	# try:
	# 	db.session.add(user)
	# 	db.session.commit()
	# except:
	# 	db.session.rollback()
	send_confirm(path=data["path"], username=data["username"], token=token, email=[data["email"], ])
	response = response_with_status(0, "Register success")
	return response


@api.route("/confirm", methods=["POST"])
def confirm():
	data = request.json
	status, statusText = User.verify_confirm_token(data["token"].encode(), data["user"])
	return response_with_status(status, statusText)


def send_confirm(path, token, username, email: list):
	message = Message(subject="心理评测系统邮箱激活", recipients=[*email])
	message.html = """
		<h2>你好，{name}</h2>
		<p>欢迎你使用吕世豪的心理评测系统，请点击下面的连接激活你的账号。</p>
		<p><a href="{path}/confirm?token={token}&user={user}">{path}/confirm?token={token}&user={user}</a></p>
		""".format(name=username, path=path, token=token, user=username)
	mail.send(message)
