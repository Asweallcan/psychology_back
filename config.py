import os


class Config:
	HOST = "127.0.0.1"
	PORT = "5000"
	DEBUG = True
	SECRETE_KEY = os.environ.get("SECRETE_KEY", "lvshihaonb")
	SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{host}/{database}".format(username="root",
	                                                                                   password="gamersky.com",
	                                                                                   host="localhost",
	                                                                                   database="py")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SERVER = "smtp.qq.com"
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_DEFAULT_SENDER = "296877137@qq.com"
	MAIL_USERNAME = "296877137@qq.com"
	MAIL_PASSWORD = "ocenipsgocozbgfh"
	CONFIRM_TOKEN = "confirm_token"
	COOKIE_TOKEN = "cookie_token"


class ProductionConfig(Config):
	SECRETE_KEY = os.environ.get("SECRETE_KEY", "different_keys")
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "mysql://")


config = {
	"default": Config,
	"development": Config,
	"production": ProductionConfig
}
