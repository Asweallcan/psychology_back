from .User import User
from app.db import db
from flask_migrate import migrate, upgrade

PaperTables = {}


def create_paper_table(table_name, cols_num: int, need_deploy: bool = False):
	"""
	动态创建试卷表的函数
	:param table_name: 创建表的表名称
	:param cols_num: 表需要多少个列
	:param need_deploy 是否需要更新数据库
	:return:
	"""
	setattr(User, table_name + "_id", db.Column(db.Integer, db.ForeignKey(table_name + ".id")))
	paper_table_class = type(table_name.capitalize(), (db.Model,), {
		"__tablename__": table_name,
		"id": db.Column(db.Integer, primary_key=True, autoincrement=True, index=True),
		"comment": db.Column(db.Text),
		"score": db.Column(db.Text),
		"class": db.Column(db.Integer),
		"user": db.relationship("User", backref=table_name, uselist=False),
		**{"col_" + str(i + 1): db.Column(db.Integer) for i in range(cols_num)}
	})
	if need_deploy:
		migrate()
		upgrade()
	return paper_table_class
