from flask import render_template, flash, redirect, request, g, url_for
from app import app, db, models
from sqlalchemy import desc
from .forms import TurkForm, CreateHITForm
from .models import Hit
import os, boto.mturk.connection, boto.mturk.question, create_HIT

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
		AWS_id = create_HIT(h.title, 
			description = form.hit_description.data, 
			keywords = form.hit_keywords.data, 
			id = h.id)
		#then need to update our DB with the task-ID as assigned by Amazon
		h.hit_id = AWS_id
		db.session.commit()
		return redirect(url_for('all_hits'))

	
@app.route('/hits/<hit_id>', methods=['GET', 'POST']) #display page for a particular HIT (POST not allowed until Turk accepts job and worker_id is provided by the get request) | no login required
def hit_consignment(hit_id):
    form = TurkForm()
    return render_template('task.html', \
                            provided_link="http://www.fbschedules.com/ncaa-16/2016-ucla-bruins-football-schedule.php", \
                            provided_description="UCLA Bruins Football Schedule",
                            hit_id = hit_id,
                            form=form)
