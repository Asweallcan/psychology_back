import os
import pandas as pd
from flask import request
from . import api
from ..models import Paper
from ..decorators import login_require, admin_require
from ..utils import response_with_status, auto_commit_db
from ..db import db


@api.route("/paper", methods=["GET", "POST", "PUT", "DELETE"])
def paper():
	if request.method == "GET":
		return paper_list()
	elif request.method == "POST":
		return add_paper()
	elif request.method == "PUT":
		return edit_paper()
	elif request.method == "DELETE":
		return delete_paper()


@login_require
def paper_list():
	"""
	获取试卷信息的接口参数：
		page?: 第几页
		pageSize?: 一页多少个
	返回：
		total: 试卷的总量
		list: [paper.info_to_json]
	"""
	page = request.args.get("page", 1, int)
	pageSize = request.args.get("pageSize", 10, int)
	data = {
		"total": Paper.query.count(),
		"list": [paper.info_to_json() for paper in Paper.query.paginate(page=page, per_page=pageSize).items]
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
		status: -1 paper_name 重复 / -2 文件解析失败 / 0 成功
		statusText:
		data:
	"""
	data = request.json
	file_str = "./uploads/{filename}"
	file_path = os.path.abspath(file_str.format(filename=data["filename"]))
	df = pd.DataFrame(pd.read_excel(file_path))
	if data.get("paper_name"):
		if Paper.query.filter_by(paper_name=data["paper_name"]).first():
			return response_with_status(-1, "Duplicate table name")
	elif Paper.query.filter_by(paper_name=df["paper_name"].astype("str").values[0]).first():
		return response_with_status(-1, "Duplicate table name")
	fields = Paper.get_fields()
	paper = Paper()
	try:
		for field in fields:
			setattr(paper, field, "@".join(df[field].dropna().astype("str").map(str.strip).values))
		for field in ["paper_name", "description", "filename"]:
			if data.get(field):
				setattr(paper, field, data.get(field))
	except:
		return response_with_status(-2, "File parse error")
	extname = "." + paper.filename.split(".").pop()
	file_path = os.path.abspath(file_str.format(filename=paper.filename))
	new_file_path = os.path.abspath(file_str.format(filename=paper.paper_name)) + extname
	os.rename(file_path, new_file_path)
	paper.filename = paper.paper_name + extname
	with auto_commit_db():
		db.session.add(paper)
	return response_with_status(0, "Success")


@login_require
@admin_require
def delete_paper():
	"""
	删除试卷接口参数:
		papers: number[];
	返回参数:
		status: 0 成功
		statusText:
		data:
	"""
	data = request.json
	file_str = "./uploads/{filename}"
	papers = Paper.query.filter(Paper.id.in_(data["papers"])).all()
	with auto_commit_db():
		for paper in papers:
			db.session.delete(paper)
			os.unlink(os.path.abspath(file_str.format(filename=paper.filename)))
	return response_with_status(0, "Success")


@login_require
@admin_require
def edit_paper():
	"""
	添加试卷接口参数:
		paper_name?: 试卷的名称
		description?: 试卷的描述
		id: 修改试卷的id
	返回参数:
		status:  -1 paper_name重复 /  0 成功
		statusText:
		data:
	"""
	data = request.json
	paper = Paper.query.filter_by(id=data["id"]).first()
	file_str = "./uploads/{filename}"
	if "paper_name" in data["fields"]:
		paper_name = data["values"][data["fields"].index("paper_name")]
		if Paper.query.filter_by(paper_name=paper_name).first():
			return response_with_status(-1, "Duplicate paper name")
		extname = "." + paper.filename.split(".").pop()
		file_path = os.path.abspath(file_str.format(filename=paper.filename))
		new_file_path = os.path.abspath(file_str.format(filename=paper_name)) + extname
		paper.paper_name = paper_name
		paper.filename = paper_name + extname
		os.rename(file_path, new_file_path)
	if "description" in data["fields"]:
		paper.description = data["values"][data["fields"].index("description")]
	sql = "UPDATE papers SET paper_name='{paper_name}',filename='{filename}',description='{description}' WHERE id={id}".format(
		paper_name=paper.paper_name, filename=paper.filename, description=paper.description, id=paper.id)
	db.session.execute(sql)
	db.session.commit()
	return response_with_status(0, "Success")
