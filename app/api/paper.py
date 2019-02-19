import os
import time
import pandas as pd
from flask import request
from . import api
from ..models import PaperInfo, User
from ..decorators import login_require, admin_require
from ..utils import response_with_status
from ..db import db


@api.route("/paper_list")
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
		"total": PaperInfo.query.count(),
		"list": [paper.info_to_json(user) for paper in PaperInfo.query.paginate(page=page, per_page=pageSize).items]
	}
	return response_with_status(0, "Success", data)


@api.route("/upload_paper", methods=["POST"])
@login_require
@admin_require
def upload_paper():
	paper_file = request.files["paper_file"]
	extname = paper_file.filename.split(".").pop()
	filename = str(int(time.time())) + "." + extname
	upload_path = os.path.abspath("./uploads/{filename}".format(filename=filename))
	paper_file.save(upload_path)
	return response_with_status(0, "Success", {"filename": filename})


@api.route("/add_paper", methods=["POST"])
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
	if PaperInfo.query.filter_by(table_name=df["table_name"].values[0]).first():
		return response_with_status(-1, "Duplicate table name")
	fields = PaperInfo.get_fields()
	paper = PaperInfo()
	try:
		for field in fields:
			setattr(paper, field, "@".join(df[field].dropna().map(str).map(str.strip).values))
		for field in ["paper_name", "description"]:
			if field in data:
				setattr(paper, field, data[field])
	except:
		return response_with_status(-2, "File parse error")
	try:
		db.session.add(paper)
		db.session.commit()
	except:
		db.session.rollback()
		return "", 500
	return response_with_status(0, "Success")
