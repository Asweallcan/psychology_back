from . import api
from ..decorators import login_require, admin_require
from ..utils import response_with_status
from flask import request
import os
import time


@api.route("/upload", methods=["POST"])
@login_require
@admin_require
def upload_paper():
	paper_file = request.files["file"]
	extname = "." + paper_file.filename.split(".").pop()
	filename = str(int(time.time())) + extname
	upload_path = os.path.abspath("./uploads/{filename}".format(filename=filename))
	paper_file.save(upload_path)
	return response_with_status(0, "Success", {"filename": filename})
