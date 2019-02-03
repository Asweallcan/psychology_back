import os


class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY", "lvshihaonb")
	SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{host}/{database}".format(username="root",
	                                                                                   password="gamersky.com",
	                                                                                   host="localhost",
	                                                                                   database="learnpython")
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "mysql://")


config = {
	"default": Config,
	"development": Config,
	"production": ProductionConfig
}
