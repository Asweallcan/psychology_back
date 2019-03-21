from flask import Flask
from config import config
import pymysql
from .models import User, Paper, Grade, rb_users_papers
from .db import db
from .mail import mail
from .api import api as api_blueprint
import os

pymysql.install_as_MySQLdb()


def create_app(config_name):
	app_path = os.path.dirname(__file__)
	static_path = os.path.abspath(os.path.join(app_path, "../uploads"))
	app = Flask(__name__, template_folder=static_path, static_folder=static_path, static_url_path="")
	app.config.from_object(config[config_name])
	db.init_app(app)
	mail.init_app(app)
	app.register_blueprint(api_blueprint, url_prefix="/api")
	return app
