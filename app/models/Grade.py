from ..db import db


class Grade(db.Model):
	__tablename__ = "grades"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	answers = db.Column(db.Text)
	score = db.Column(db.String(32))
	level = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
	paper_id = db.Column(db.Integer, db.ForeignKey("papers.id", ondelete="CASCADE"))
