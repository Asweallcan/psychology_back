import threading
from flask import make_response, jsonify, copy_current_request_context
from flask_mail import Message
from .mail import mail


def response_with_status(status, statusText, data=None):
	if data is None:
		data = {}
	response = make_response(jsonify({"status": status, "statusText": statusText, "data": data}))
	return response


def send_confirm(path, token, username, forget: bool, recipients: list,
                 sender):
	"""
	:param path: 目标系统的url地址
	:param token: 邮箱验证token
	:param username: 用户名
	:param forget: 是否是忘记密码的邮件
	:param recipients: 接收人
	:param sender: 发送者，默认读取appConfig文件中的配置
	"""
	message = Message(subject="心理评测系统邮箱激活", recipients=[*recipients, ], sender=sender)
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

	@copy_current_request_context
	def send_async_email(message):
		mail.send(message)

	t = threading.Thread(target=send_async_email, args=[message])
	t.start()



