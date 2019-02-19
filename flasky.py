from app import create_app, db, PaperTables, PaperInfo, create_paper_table, User
from flask_migrate import Migrate
import traceback
import os

app = create_app(os.environ.get("CONFIG_NAME", "default"))

migrate = Migrate()
migrate.init_app(app, db)

with app.app_context():
	try:
		for info in PaperInfo.query.all():
			PaperTables[info.table_name] = create_paper_table(info.table_name, info.cols_num)
	except Exception:
		traceback.print_exc()


@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, PT=PaperTables, PI=PaperInfo)


@app.cli.command()
def test():
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=2).run(tests)
