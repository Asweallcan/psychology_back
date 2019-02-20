from ..db import db


class Paper(db.Model):
	__tablename__ = "papers"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, default=1)
	paper_name = db.Column(db.String(32), nullable=False, index=True, primary_key=True)
	type = db.Column(db.String(32), default="psychology")
	description = db.Column(db.String(32))
	filename = db.Column(db.String(32))
	average = db.Column(db.String(32))
	cols_num = db.Column(db.Integer)
	questions = db.Column(db.Text, nullable=False)
	questions_img = db.Column(db.Text)
	answers = db.Column(db.Text, nullable=False)
	answers_img = db.Column(db.Text)
	answers_score = db.Column(db.Text)
	answers_multiple = db.Column(db.Text)
	score_attrs = db.Column(db.Text)
	comments_condition = db.Column(db.Text)
	comments = db.Column(db.Text)
	grades = db.relationship("Grade", backref="paper", lazy="dynamic")

	def __setattr__(self, key, value):
		"""
		当设置questions属性的时候自动设置cols_num
		"""
		if key == "table_name":
			if not value.startswith("paper_"):
				value = "paper_" + value
		if key == "questions":
			self.cols_num = len(value.split("@"))
		self.__dict__[key] = value

	def to_json(self):
		"""
		将试卷格式化为json
		:return: object
		"""
		questions = self.questions_to_json()
		answers = self.answers_to_json()
		return [{**questions[i], **answers[i]} for i in range(self.cols_num)]

	def info_to_json(self, user):
		"""
		试卷信息json化
		:param user: 用户信息
		:return:
		"""
		return {
			"id": self.id,
			"paper_name": self.paper_name,
			"description": self.description,
			"attended": user.papers.filter_by(id=self.id).first() is not None,
			"attend_count": len(self.users.all()),
			"download_url": "/uploads/{filename}".format(filename=self.filename)
		}

	def questions_to_json(self):
		questions = self.questions.split("@")
		questions_img = self.questions_img.split("@")
		return [
			{
				"question": questions[i],
				"question_img": "" if questions_img[i] == "_" else questions_img[i]
			} for i in range(self.cols_num)
		]

	def answers_to_json(self):
		answers = self.answers.split("@")
		answers_img = self.answers_img.split("@")
		answers_multiple = self.answers_multiple.split("@")
		return [
			{
				"answers": answers[i].split("/"),
				"answers_img": answers_img[i].split("/"),
				"multiple": True if int(answers_multiple[i]) != 0 else False
			} for i in range(self.cols_num)
		]

	@staticmethod
	def get_fields():
		"""
		获取从excel表格中需要获取的参数
		:return:
		"""
		return ["paper_name", "type", "description", "questions", "questions_img", "answers",
		        "answers_img", "answers_score", "answers_multiple", "score_attrs", "comments_condition", "comments"]
