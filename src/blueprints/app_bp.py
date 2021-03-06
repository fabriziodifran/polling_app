from flask import Blueprint, render_template, request, redirect
from models import Polls, Options, Votes, db
from datetime import datetime, timedelta

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
		creation_date = datetime.now()
		expiration_time = int(request.form.get('expiration_time'))
		
		if expiration_time>0:
			time_delta = timedelta(hours=expiration_time)
			expiration_date = creation_date + time_delta
			expiration_date = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
		else:
			expiration_date = None


		if len(poll_options)==4:
			poll_opt1, poll_opt2, poll_opt3, poll_opt4 = poll_options
		
		elif len(poll_options)==3:
			poll_opt1, poll_opt2, poll_opt3 = poll_options
			poll_opt4 = None
		
		elif len(poll_options)==2:
			poll_opt1, poll_opt2 = poll_options
			poll_opt3 = None
			poll_opt4 = None


		new_poll = Polls(title=poll_title, tags=poll_tags,
						creation_date=creation_date.strftime("%Y-%m-%d %H:%M:%S"),
						expiration_date=expiration_date)
		
		new_options = Options(option1=poll_opt1,
							option2=poll_opt2,
							option3=poll_opt3,
							option4=poll_opt4) 
		
		db.session.add(new_poll)
		db.session.add(new_options)
		db.session.commit()
		return render_template('mensaje.html', status='Encuesta creada con éxito', msg='Podés crear otras encuestas o votar')
	
	else:
		return render_template('crear-encuesta.html')

@bp.route('/polls', methods=['GET', 'POST'])
def list_polls():
	tags = request.form.get('tags')
	if tags:
		tag_list = [x.strip() for x in tags.split(',')]
		all_polls = []
		
		for tag in tag_list:
			all_polls+=Polls.query.filter(Polls.tags.contains(tag)).all()

		all_polls = list(set(all_polls))
		
		return render_template('encuestas.html', polls=all_polls)

	else:
		all_polls = Polls.query.order_by(Polls.id.desc()).all()
		return render_template('encuestas.html', polls=all_polls)

@bp.route('/vote/<id>', methods=['GET'])
def vote(id):
	poll = Polls.query.filter(Polls.id==id)[0]
	options = Options.query.filter(Options.id==id)[0]

	options_list = [options.option1, options.option2,options.option3, options.option4]
	options_list = [i for i in options_list if i]
	option_votes = []

	for op in options_list:
		op_votes = Votes.query.filter(Votes.poll_id == poll.id).filter(Votes.vote == op).count()
		option_votes.append([op, op_votes])



	return render_template('votacion.html', title=poll.title, options=options_list,
							id=poll.id, votes=option_votes)

@bp.route('/vote_processing', methods=['POST'])
def vote_processing():
	poll_id = request.form['id']
	try:
		vote = request.form['options']
		new_vote = Votes(poll_id=poll_id, vote=vote)
		db.session.add(new_vote)
		db.session.commit()
		return render_template('mensaje.html', status='Voto guardado!', msg="Gracias por participar")
	
	except:
		return render_template('mensaje.html', status='Error', msg="Debes elegir una opción", id=poll_id)



