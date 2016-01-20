from flask import render_template, flash, redirect, request, g, url_for
from app import app, db, models
from .create_HIT import create_task
from sqlalchemy import desc
from .forms import TurkForm, CreateHITForm
from .models import Hit
import os, boto.mturk.connection, boto.mturk.question

@app.route('/')
@app.route('/index') #landing page, soon to become a sign-in page 
def hello():
    return 'Greetings, Professor Falken.'

@app.route('/hits') #landing page for tasks, intended to show a table of all HITs, with links/buttons for deletion | needs login
def all_hits():
	hits = Hit.query.order_by(desc(Hit.id)).all()
	return render_template('all_hits.html', hits=hits)

@app.route('/hits/create', methods=['GET', 'POST'])  #page for creating new HITs | needs login for GET and POST
def createHIT():
	form = CreateHITForm()
	if request.method == 'GET':
		return render_template('create_HIT.html', form=form)
	if request.method == 'POST':
		#need to create with our DB first
		h = models.Hit()
		h.title = form.hit_title.data
		h.url = form.hit_url.data
		h.status = "open"
		db.session.add(h)
		db.session.commit()
		#then need to return a URL, title, keywords, bounty, used to create the HIT in Amazon
		#create_task(id, title, description, keywords)
		AWS_id = create_task(h.id, h.title, form.hit_description.data, form.hit_keywords.data.split(','))
		#then need to update our DB with the task-ID as assigned by Amazon
		h.hit_id = AWS_id
		db.session.commit()
		return redirect(url_for('all_hits')) #can be changed later

	
@app.route('/hits/<id>', methods=['GET', 'POST']) #display page for a particular HIT (POST not allowed until Turk accepts job and worker_id is provided by the get request) | no login required
def hit_consignment(id):
    form = TurkForm()
    h = models.Hit.query.get(id)
    if request.method == 'GET':
    	#get the following variables from Amazon when the GET request originates from there
    	worker_id = request.args.get("workerId")
    	assignment_id = request.args.get("assignmentId")
        task_id = request.args.get("hitId")
    	return render_template('task.html', 
                        provided_link= h.url,
                        provided_description= h.title,
                        hit_id = task_id,
                        worker_id = worker_id,
                        assignment_id = assignment_id,
                        external_submit_url = os.environ['EXTERNAL_SUBMIT_SANDBOX_URL'],
                        form=form)
    if request.method == 'POST':
    	# our parsing goes here, or data can just be entered into our db directly; data is sanitized by wtforms when .data is called
    	# need to confer with James and ask how Turk input will be ingested to the Tassl events DB
    	# need to check with field validation here
    	h.turk_input = form.turk_input.data
    	db.session.commit()
    	flash('Turk input been recorded.')
    	return redirect(url_for('all_hits'))
