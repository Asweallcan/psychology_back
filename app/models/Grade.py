from ..db import db


class Grade(db.Model):
	__tablename__ = "grades"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	finished = db.Column(db.Boolean, default=False)
	analyzed = db.Column(db.Boolean, default=False)
	above_percent = db.Column(db.Text)
	answers = db.Column(db.Text)
	score = db.Column(db.String(32))
	total_score = db.Column(db.Integer)
	level = db.Column(db.String(32))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
	paper_id = db.Column(db.Integer, db.ForeignKey("papers.id", ondelete="CASCADE"))
