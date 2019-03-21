from app import create_app, db, Paper, User, rb_users_papers
from flask_migrate import Migrate
from flask import render_template, url_for, request
import os

app = create_app(os.environ.get("CONFIG_NAME", "default"))

migrate = Migrate()
migrate.init_app(app, db)


@app.route("/")
def index():
	return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
	return render_template("index.html")


@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Paper=Paper, RB_users_papers=rb_users_papers)


@app.cli.command()
def test():
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
	app.run(app.config["HOST"], app.config["PORT"], debug=app.config["DEBUG"])
