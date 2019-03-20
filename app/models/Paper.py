from ..db import db
from .User import User
from .Registrations import rb_users_papers


class Paper(db.Model):
	__tablename__ = "papers"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	paper_name = db.Column(db.String(32), nullable=False, index=True, primary_key=True)
	type = db.Column(db.String(32), default="psychology")
	description = db.Column(db.Text)
	filename = db.Column(db.String(32))
	average = db.Column(db.Text)
	most_choice = db.Column(db.Text)
	questions = db.Column(db.Text, nullable=False)
	questions_count = db.Column(db.Integer)
	questions_img = db.Column(db.Text)
	answers = db.Column(db.Text, nullable=False)
	answers_img = db.Column(db.Text)
	answers_score = db.Column(db.Text)
	answers_multiple = db.Column(db.Text)
	score_attrs = db.Column(db.Text)
	comments_condition = db.Column(db.Text)
	comments = db.Column(db.Text)
	grades = db.relationship("Grade", backref="paper", lazy="dynamic", cascade="all, delete-orphan",
	                         passive_deletes=True)
	users = db.relationship("User", secondary=rb_users_papers, lazy="dynamic")

	def __setattr__(self, key, value):
		if key == "questions":
			self.questions_count = len(value.split("@"))
		self.__dict__[key] = value

	def to_json(self):
		"""
		将试卷格式化为json
		:return: object
		"""
		user = User.get_user_from_cookie()
		grade = self.grades.filter_by(user_id=user.id).first()
		m_answers = []
		answered_count = 0
		comment = []
		if grade:
			n_answers = grade.answers.split("@")
			for answer in n_answers:
				if answer:
					if int(answer) >= 0:
						if not grade.finished:
							answered_count += 1
						m_answers.append(int(answer))
				if not answer:
					m_answers.append(None)
			if grade.finished:
				answered_count = self.questions_count
			comments = self.comments.split("@")
			for index, level in enumerate(map(int, grade.level.split("@")) if grade.level else []):
				comment.append(comments[level - 1])
		questions = self.questions_to_json()
		answers = self.answers_to_json()
		return {
			"questions": [{**questions[i], **answers[i]} for i in range(self.questions_count)],
			"answers": m_answers,
			"answered_count": answered_count,
			"questions_count": self.questions_count,
			"finished_count": len(self.grades.filter_by(finished=True).all()),
			"paper_name": self.paper_name,
			"description": self.description,
			"average": self.average,
			"most_choice": self.most_choice,
			"score_attrs": self.score_attrs,
			"score_above": grade.above_percent if grade else "",
			"score": grade.score if grade else "",
			"comment": "。".join(comment)
		}

	def info_to_json(self):
		"""
		试卷信息json化
		"""
		user = User.get_user_from_cookie()
		grade = self.grades.filter_by(user_id=user.id).first()
		finished = False
		analyzed = False
		answered_count = 0
		if grade:
			finished = grade.finished
			analyzed = grade.analyzed
			if not finished:
				for answer in grade.answers.split("@"):
					if answer:
						if int(answer) >= 0:
							answered_count += 1
			else:
				answered_count = self.questions_count
		return {
			"id": self.id,
			"paper_name": self.paper_name,
			"description": self.description,
			"attended": answered_count > 0,
			"answered_count": answered_count,
			"questions_count": self.questions_count,
			"attend_count": len(self.users.all()),
			"download_url": "/uploads/{filename}".format(filename=self.filename),
			"finished": finished,
			"analyzed": analyzed
		}

	def questions_to_json(self):
		questions = self.questions.split("@")
		questions_img = self.questions_img.split("@")
		return [
			{
				"question": questions[i],
				"question_img": "" if questions_img[i] == "_" else questions_img[i]
			} for i in range(self.questions_count)
		]

	def answers_to_json(self):
		answers = self.answers.split("@")
		answers_img = self.answers_img.split("@")
		answers_multiple = self.answers_multiple.split("@")
		return [
			{
				"answers": answers[i].split("/"),
				"answers_img": answers_img[i].split("*"),
				"multiple": int(float(answers_multiple[i])) != 0
			} for i in range(self.questions_count)
		]

	@staticmethod
	def get_fields():
		"""
		获取从excel表格中需要获取的参数
		:return:
		"""
		return ["paper_name", "type", "description", "questions", "questions_img", "answers",
		        "answers_img", "answers_score", "answers_multiple", "score_attrs", "comments_condition", "comments"]
