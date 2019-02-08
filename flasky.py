from app import create_app, db, mail, PaperTables, PaperInfo, User, create_paper_table
from flask_migrate import Migrate
import os

migrate_app = Migrate()

app = create_app(os.environ.get("CONFIG_NAME", "default"))
migrate_app.init_app(app, db)
mail.init_app(app)

with app.app_context():
	"""
	在程序启动的时候获取试卷表的orm对象
	"""
	try:
		for info in PaperInfo.query.all():
			PaperTables[info.table_name] = create_paper_table(info.table_name, info.cols_num)
	except Exception:
		pass


@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, PaperInfo=PaperInfo, PaperTables=PaperTables)


@app.cli.command()
def test():
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=2).run(tests)
