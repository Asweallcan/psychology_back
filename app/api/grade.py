from . import api
from ..db import db
from ..decorators import admin_require, login_require
from ..models import Paper, User, Grade
from ..utils import response_with_status
from flask import request, copy_current_request_context
from sqlalchemy import or_
from threading import Thread


@api.route("/grade", methods=["GET", "POST", "PUT", "DELETE"])
def grade():
	if request.method == "GET":
		return grade_list()


@login_require
@admin_require
@api.route("/grade_info")
def grade_info():
	papers = Paper.query.all()
	return response_with_status(0, "Success", {
		"papers_name": [paper.paper_name for paper in papers],
		"papers_attrs": [paper.score_attrs.split("@") for paper in papers],
		"conditions": [paper.comments_condition.split("@") for paper in papers]
	})


@login_require
@admin_require
def grade_list():
	page = request.args.get("page", default=1, type=int)
	pageSize = request.args.get("pageSize", default=10, type=int)
	paper_name = request.args.get("paperName", type=str)
	level = None if request.args.get("condition", type=int) == -1 else request.args.get("condition", type=int) + 1
	search = request.args.get("search", type=str)
	paper = Paper.query.filter_by(paper_name=paper_name).first()
	d = lambda grade: {
		"username": User.query.filter_by(id=grade.user_id).first().username,
		"paper_name": grade.paper.paper_name,
		"scores": grade.score.split("@"),
		"total_score": grade.total_score,
		"id": grade.id
	}
	if paper_name and not search:
		if level:
			l = [d(grade) for grade in
			     paper.grades.order_by(Grade.total_score.desc()).paginate(page=page, per_page=pageSize).items
			     if level in list(map(int, grade.level.split("@")))]
			return response_with_status(0, "Success", {"total": len(l), "list": l})
		l = [d(grade) for grade in
		     paper.grades.order_by(Grade.total_score.desc()).paginate(page=page, per_page=pageSize).items]
		return response_with_status(0, "Success", {"total": len(l), "list": l})
	user = User.query.filter(or_(User.username == search, User.email == search)).first()
	if search and not paper_name:
		if user:
			l = [d(grade) for grade in user.grades.order_by(Grade.total_score.desc()).all()]
			return response_with_status(0, "Success", {"total": len(l), "list": l})
	if search and paper_name:
		if user:
			if level:
				l = [d(grade) for grade in
				     user.grades.filter_by(paper_id=paper.id).order_by(Grade.total_score.desc()).paginate(page=page,
				                                                                                          per_page=pageSize).items
				     if level in list(map(int, grade.level.split("@")))]
				return response_with_status(0, "Success", {"total": len(l), "list": l})
			l = [d(grade) for grade in
			     user.grades.filter_by(paper_id=paper.id).order_by(Grade.total_score.desc()).paginate(page=page,
			                                                                                          per_page=pageSize).items]
			return response_with_status(0, "Success", {"total": len(l), "list": l})
	return response_with_status(0, "Success", {"total": 0, "list": []})


@login_require
@admin_require
@api.route("/add_condition", methods=["POST"])
def add_condition():
	data = request.json
	condition = data["condition"]
	comment = data.get("comment", None)
	paper_name = data["paper_name"]
	paper = Paper.query.filter_by(paper_name=paper_name).first()
	if (condition in paper.comments_condition.split("@")):
		return response_with_status(-1, "Duplicate condition")
	paper.comments_condition = paper.comments_condition + "@" + condition
	if comment:
		paper.comments = paper.comments + "@" + comment
	db.session.execute(
		"UPDATE papers SET comments_condition='{comments_condition}',comments='{comments}' WHERE paper_name='{paper_name}'".format(
			comments_condition=paper.comments_condition, comments=paper.comments, paper_name=paper.paper_name
		))
	db.session.commit()

	@copy_current_request_context
	def analyze():
		data = request.json
		paper = Paper.query.filter_by(paper_name=data["paper_name"]).first()
		for grade in paper.grades:
			attrs_score = list(map(int, grade.score.split("@")))
			flag = True
			for index_i, condition_i in enumerate(condition.split("/")):
				if not condition_i:
					continue
				score = attrs_score[index_i]
				scores = list(map(int, condition_i.split("#")))
				if not (scores[1] > score > scores[0]):
					flag = False
					break
			if flag:
				grade.level = grade.level + "@" + str(len(paper.comments_condition.split("@")))
				db.session.execute(
					"UPDATE grades SET level='{level}' WHERE id={id}".format(level=grade.level, id=grade.id))
				db.session.commit()

	t = Thread(target=analyze)
	t.start()
	return response_with_status(0, "Success")
