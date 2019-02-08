from flask import request, make_response, jsonify


def response_with_status(status, statusText, data=None):
	if data is None:
		data = {}
	response = make_response(jsonify({"status": status, "statusText": statusText, "data": data}))
	return response


def get_user(response):
	user = request.cookies.get("user")
	if not user:
		response.headers["redirect"] = "login"
		return None
	return user
