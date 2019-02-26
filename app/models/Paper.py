from ..db import db
from .User import User


class Paper(db.Model):
	__tablename__ = "papers"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	paper_name = db.Column(db.String(32), nullable=False, index=True, primary_key=True)
	type = db.Column(db.String(32), default="psychology")
	description = db.Column(db.Text)
	filename = db.Column(db.String(32))
	average = db.Column(db.String(32))
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

	def __setattr__(self, key, value):
		"""
		当设置questions属性的时候自动设置questions_count
		"""
		if key == "questions":
			self.questions_count = len(value.split("@"))
		self.__dict__[key] = value

	def to_json(self):
		"""
		将试卷格式化为json
		:return: object
		"""
		user = User.get_user_from_cookie()
		paper = user.papers.filter_by(id=self.id).first()
		m_answers = []
		answered_count = 0
		if paper:
			grade = paper.grades.filter_by(user_id=user.id).first()
			m_answers = grade.answers.split("@")
			answered_count = len(m_answers)
		questions = self.questions_to_json()
		answers = self.answers_to_json()
		return {
			"questions": [{**questions[i], **answers[i]} for i in range(self.questions_count)],
			"answers": m_answers,
			"answered_count": answered_count,
			"questions_count": self.questions_count,
			"paper_name": self.paper_name,
			"description": self.description
		}

	def info_to_json(self):
		"""
		试卷信息json化
		:param user: 用户信息
		:return:
		"""
		user = User.get_user_from_cookie()
		paper = user.papers.filter_by(id=self.id).first()
		answered_count = 0
		finished = False
		if paper:
			grade = paper.grades.filter_by(user_id=user.id).first()
			answered_count = len(grade.answers.split("@"))
			finished = answered_count == self.questions_count
		return {
			"id": self.id,
			"paper_name": self.paper_name,
			"description": self.description,
			"attended": answered_count != 0,
			"answered_count": answered_count,
			"questions_count": self.questions_count,
			"attend_count": len(self.users.all()),
			"download_url": "/uploads/{filename}".format(filename=self.filename),
			"finished": finished
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
				"answers_img": answers_img[i].split("/"),
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
