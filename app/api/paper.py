from flask import request
from uuid import uuid1
from . import api
from ..models import PaperInfo
from ..decorators import login_require, admin_require
from ..utils import get_user_from_cookie, response_with_status
import os


@api.route("/paper_list")
@login_require
def paper_info():
	user = get_user_from_cookie()
	return response_with_status(0, "Success", [paper.info_to_json(user) for paper in PaperInfo.query.all()])


@api.route("/upload_paper", methods=["POST"])
@login_require
@admin_require
def upload_paper():
	paper_file = request.files["paper_file"]
	extname = paper_file.filename.split(".").pop()
	print(extname)
	print(os.path.abspath("../uploads/" + str(uuid1()) + "." + extname))
	# upload_path = os.path.abspath("../../uploads/" + str(uuid1()))
	# paper_file.save(upload_path)
	return "Ok"
