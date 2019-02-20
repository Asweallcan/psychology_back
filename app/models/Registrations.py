from ..db import db

rb_users_papers = db.Table(
	"rb_users_papers",
	db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
	db.Column("paper_id", db.Integer, db.ForeignKey("papers.id"), primary_key=True)
)
