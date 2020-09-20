import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Polls(db.Model):
	__tablename__ = 'polls'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	tags = db.Column(db.String(200), default='N/A')
	author = db.Column(db.String(20), default='N/A')
	creation_date = db.Column(db.DateTime, nullable=False)
	expiration_date = db.Column(db.DateTime, nullable=True)

	def __repr__(self):
		return f'Encuesta Nº {self.id}'

class Options(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	option1 = db.Column(db.String(100), nullable=False)
	option2 = db.Column(db.String(100), nullable=False)
	option3 = db.Column(db.String(100), default=None)
	option4 = db.Column(db.String(100), default=None)

	def __repr__(self):
		return self.id

class Votes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	poll_id = db.Column(db.Integer)
	vote = db.Column(db.String(100))

	def __repr__(self):
		return self.id