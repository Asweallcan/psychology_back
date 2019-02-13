from flask import Flask
from config import config
import pymysql
from .models import User, PaperTables, PaperInfo, create_paper_table
from .db import db
from .mail import mail
from .api import api as api_blueprint

pymysql.install_as_MySQLdb()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	db.init_app(app)
	mail.init_app(app)
	app.register_blueprint(api_blueprint, url_prefix="/api")
	return app
