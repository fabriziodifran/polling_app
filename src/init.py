from flask import Flask
import flask_sqlalchemy

from models import db
import config

def create_app():
	flask_app = Flask(__name__)
	flask_app.config.from_object("config.Config")
	flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	flask_app.app_context().push()
	db.init_app(flask_app)
	db.create_all()
	return flask_app
