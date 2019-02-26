from . import api
from ..db import db
from ..decorators import login_require
from ..utils import response_with_status
from ..models import Paper
from flask import request


@api.route("/test/<int:id>", methods=["GET", "POST"])
def test(id):
	if request.method == "GET":
		return get_test_paper(id)
	elif request.method == "POST":
		pass


@login_require
def get_test_paper(id):
	return response_with_status(0, "Success", Paper.query.filter_by(id=id).first().to_json())
