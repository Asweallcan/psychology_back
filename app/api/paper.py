import os
import time
import pandas as pd
import traceback
from flask import request
from . import api
from ..models import Paper, User
from ..decorators import login_require, admin_require
from ..utils import response_with_status, error_response
from ..db import db


@api.route("/paper", methods=["GET", "POST", "PUT", "DELETE"])
def paper():
	if request.method == "GET":
		return paper_info()
	elif request.method == "POST":
		return add_paper()
	elif request.method == "PUT":
		return edit_paper()
	elif request.method == "DELETE":
		return delete_paper()


@api.route("/upload_paper", methods=["POST"])
@login_require
@admin_require
def upload_paper():
	paper_file = request.files["paper_file"]
	extname = "." + paper_file.filename.split(".").pop()
	filename = str(int(time.time())) + extname
	upload_path = os.path.abspath("./uploads/{filename}".format(filename=filename))
	paper_file.save(upload_path)
	return response_with_status(0, "Success", {"filename": filename})


@login_require
def paper_info():
	"""
	获取试卷信息的接口参数：
		无
	返回：
		total: 试卷的总量
		list: [paper.info_to_json]
	"""
	page = request.args.get("page", 1, int)
	pageSize = request.args.get("pageSize", 10, int)
	user = User.get_user_from_cookie()
	data = {
		"total": Paper.query.count(),
		"list": [paper.info_to_json(user) for paper in Paper.query.paginate(page=page, per_page=pageSize).items]
	}
	return response_with_status(0, "Success", data)


@login_require
@admin_require
def add_paper():
	"""
	添加试卷接口参数:
		paper_name?: 试卷的名称
		description?: 试卷的描述
		filename: 试卷上传的文件名称
	返回参数:
		status: -1 插入数据库失败 / -2 table name重复 / -3 文件解析失败 / 0 成功
		statusText:
		data:
	"""
	data = request.json
	file_path = os.path.abspath("./uploads/{filename}".format(filename=data["filename"]))
	df = pd.DataFrame(pd.read_excel(file_path))
	if Paper.query.filter_by(paper_name=df["paper_name"].values[0]).first():
		return response_with_status(-1, "Duplicate table name")
	if data.get("paper_name") and Paper.query.filter_by(paper_name=data["paper_name"]).first():
		return response_with_status(-1, "Duplicate table name")
	fields = Paper.get_fields()
	paper = Paper()
	try:
		for field in fields:
			setattr(paper, field, "@".join(df[field].dropna().map(str).map(str.strip).values))
		for field in ["paper_name", "description", "filename"]:
			if data.get(field):
				setattr(paper, field, data.get(field))
	except:
		return response_with_status(-2, "File parse error")
	extname = "." + paper.filename.split(".").pop()
	file_str = "./uploads/{filename}"
	os.rename(file_str.format(filename=paper.filename), file_str.format(filename=paper.paper_name) + extname)
	paper.filename = paper.paper_name + extname
	try:
		db.session.add(paper)
		db.session.commit()
	except:
		db.session.rollback()
		return error_response()
	return response_with_status(0, "Success")


@login_require
@admin_require
def delete_paper():
	data = request.json
	paper = Paper.query.filter_by(id=data["id"]).first()
	file_path = os.path.abspath("./uploads/{filename}".format(filename=paper.filename))
	try:
		os.unlink(file_path)
		db.session.delete(paper)
		db.session.commit()
	except:
		traceback.print_exc()
		db.session.rollback()
		return error_response()
	return response_with_status(0, "Success")


@login_require
@admin_require
def edit_paper():
	pass
