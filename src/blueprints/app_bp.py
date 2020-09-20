from flask import Blueprint, render_template, request, redirect
from models import Polls, db
from datetime import date

bp = Blueprint('blueprint', __name__, template_folder='../templates')

@bp.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@bp.route('/create_poll', methods=['POST', 'GET'])
def create_poll():
	if request.method == 'POST':
		poll_title = request.form.get('title')
		poll_options = request.form.getlist('option')
		poll_tags = request.form.get('tags')

		if len(poll_options)==4:
			poll_opt1, poll_opt2, poll_opt3, poll_opt4 = poll_options
		
		elif len(poll_options)==3:
			poll_opt1, poll_opt2, poll_opt3 = poll_options
			poll_opt4 = None
		
		elif len(poll_options)==2:
			poll_opt1, poll_opt2 = poll_options
			poll_opt3 = None
			poll_opt4 = None


		new_poll = Polls(title=poll_title, tags=poll_tags, creation_date=date.today(),
						expiration_date=None, option1=poll_opt1, option2=poll_opt2,
						option3=poll_opt3, option4=poll_opt4)
		
		db.session.add(new_poll)
		db.session.commit()
		return redirect('/')
	
	else:
		return render_template('crear-encuesta.html')

@bp.route('/polls', methods=['GET'])
def list_polls():
	all_polls = Polls.query.order_by(Polls.creation_date).all()
	return render_template('encuestas.html', polls=all_polls)