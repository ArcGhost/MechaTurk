from flask import render_template, flash, redirect, request, g, url_for
from app import app, db, models
from .create_HIT import create_task, mturk
from sqlalchemy import desc
from .forms import TurkForm, CreateHITForm, UsernamePasswordForm, FeedbackForm, EventForm
from .models import Hit, User
import os, boto.mturk.connection, boto.mturk.question
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
import datetime, json


@app.template_filter('days_ago') #this will make a function available to templates
def days_ago(t=datetime.timedelta(0)):
	diff = (datetime.datetime.now() - t)
	return diff.days


@app.before_request # functions decorated with before_request run before the view function when request is received
def before_request():
	g.user = current_user #g global is setup by Flask to store and share data during the life of a request
	#current_user global is set by Flask-Login; we put a copy in the g object so that all requests have access to the logged-in user, even inside templates
	g.acct_bal = mturk.get_account_balance() #get up-to-date balances


@app.context_processor #this function, decorated with context_processor, will run before the templating code, making g.acct_bal available to all views
def inject_acct_bal():
	return dict(acct_bal=g.acct_bal) 


@app.route('/', methods=["GET", "POST"]) #signin page
@app.route('/index', methods=["GET", "POST"])
def index():
	form = UsernamePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first_or_404()
		if user.is_correct_password(form.password.data):
			login_user(user)
			return redirect(url_for('all_hits'))
		else:
			flash('Sign-in error. Please check your input and try again.')
			return redirect(url_for('index'))
	return render_template('signin.html', form=form)


@app.route('/signout') #signout page
def signout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/hits') #dashboard for all HITs
@login_required
def all_hits():
	hits = Hit.query.order_by(desc(Hit.id)).all()
	return render_template('all_hits.html', hits=hits)


@app.route('/hits/<id>') #admin view for an HIT
@login_required
def view_hit(id):
	h = models.Hit.query.get(id)
	form = FeedbackForm()
	events = h.events.all()
	events = sorted(events, key = lambda x:x.id) #sort by id
	#print events
	return render_template('view_hit.html', 
						hit = h,
						events = events, 
						form = form)


@app.route('/hits/<id>/<judgement>') #routes for approval/rejection of Turk work
@login_required
def approve_or_reject(id, judgement):
	h = models.Hit.query.get(id)
	form = FeedbackForm()
	assignment = mturk.get_assignments(h.hit_id, status='Submitted')[0] #get the first submitted assignment for the hit (this will exclude approved and rejected assignments)
	#ass_id = assignment.AssignmentId #fetch the id
	ass_id = h.assignment_id
	feedback = form.feedback.data #fetch the Tassl feedback
	h.status = judgement
	db.session.commit()
	if judgement == 'approved':
		mturk.approve_assignment(ass_id, feedback)
		#delivery to James' portal to happen here
	elif judgement == 'rejected':
		mturk.reject_assignment(ass_id, feedback)
		mturk.extend_hit(h.hit_id, 1) #adds one more assignment under current hit, so that it can still be done without creating another hit
	return redirect(url_for('all_hits'))


@app.route('/hits/create', methods=['GET', 'POST'])  #page for creating new HITs | needs login for GET and POST
@login_required
def createHIT():
	form = CreateHITForm()
	if request.method == 'GET':
		return render_template('create_HIT.html', form=form)
	if request.method == 'POST':
		h = models.Hit() #need to create with our DB first
		h.title = form.hit_title.data
		h.url = form.hit_url.data
		h.status = "open"
		h.bounty = form.hit_bounty.data
		h.instructions = form.hit_instructions.data
		h.keywords = form.hit_keywords.data
		h.created_at = datetime.datetime.now()
		h.deadline = int(form.hit_deadline.data)
		h.school = form.hit_school.data
		db.session.add(h)
		db.session.commit()
		#then need to return a URL, title, keywords, bounty, used to create the HIT in Amazon
		#create_task(id, title, description, keywords, deadline, bounty)
		AWS_id = create_task(h.id, h.title, h.instructions, form.hit_keywords.data.split(','), h.deadline, h.bounty)


		#then need to update our DB with the task-ID as assigned by Amazon
		h.hit_id = AWS_id
		db.session.commit()
		return redirect(url_for('all_hits')) #can be changed later

	
@app.route('/consignment/<id>', methods=['GET', 'POST']) #display page for a particular HIT (POST not allowed until Turk accepts job and worker_id is provided by the get request) | no login required
def hit_consignment(id):
	form = EventForm()
	h = models.Hit.query.get(id)
	events = range(2)
	if request.method == 'GET':
		#get the following variables from Amazon when the GET request originates from there
		if request.args.get("workerId") != 'ASSIGNMENT_ID_NOT_AVAILABLE':
			h.worker_id = request.args.get("workerId")
		if request.args.get("assignmentId") != None:
			h.assignment_id = request.args.get("assignmentId")
		db.session.commit()
		print "worker id: ", h.worker_id
		print "assignment id: ", h.assignment_id
		task_id = request.args.get("hitId") #get hitID, as assigned by amazon
		return render_template('test.html', 
						id = id,
						hit = h,
						hit_id = task_id,
						provided_link= h.url,
						provided_description= h.title,
						worker_id = h.worker_id,
						assignment_id = h.assignment_id,
						external_submit_url = os.environ['EXTERNAL_SUBMIT_SANDBOX_URL'],
						events = events,
						form=form)
	if request.method == 'POST':
		h.status = 'reviewable'
		print request.args
		print "worker id: ", h.worker_id
		print "assignment id: ", h.assignment_id
		db.session.commit()
		#flash('Turk input been recorded.')
		return 'success'


@app.route('/hits/recreate/<id>', methods=['GET', 'POST'])
@login_required
def recreateHIT(id):
	h = models.Hit.query.get(id)
	h.status = 'expired' #set HIT to 'expired' in our DB
	db.session.commit()
	mturk.expire_hit(h.hit_id) #expire old HIT in Amazon
	form = CreateHITForm()
	if request.method == 'GET': #populate with existing data
		form.hit_title.data = h.title
		form.hit_url.data = h.url
		form.hit_instructions.data = h.instructions
		form.hit_bounty.data = h.bounty
		return render_template('create_HIT.html', form=form)
	if request.method == 'POST':
		q = models.Hit() #need to create a new model with our DB first
		q.title = form.hit_title.data
		q.url = form.hit_url.data
		q.status = "open"
		q.bounty = form.hit_bounty.data
		q.instructions = form.hit_instructions.data
		q.created_at = datetime.datetime.now()
		q.deadline = int(form.hit_deadline.data)
		db.session.add(q)
		db.session.commit()
		#then need to return a URL, title, keywords, bounty, used to create the HIT in Amazon
		#create_task(id, title, description, keywords, bounty)
		AWS_id = create_task(q.id, q.title, q.instructions, form.hit_keywords.data.split(','), q.deadline, q.bounty)
		#then need to update our DB with the task-ID as assigned by Amazon
		q.hit_id = AWS_id
		db.session.commit()
		return redirect(url_for('all_hits')) #can be changed later


@app.route('/logevent', methods=['POST'])
def logevent():
	eventData = request.get_json() # puts request JSON in a python dict
	e = models.Event()
	for key in eventData:
			setattr(e, key, eventData[key])
	e.hit_id = eventData['eventHit']
	db.session.add(e)
	db.session.commit()
	response_html = "<td>" + eventData['event_name'] + "</td><td>" + eventData['start_date'] + "</td></tr>"
	return response_html


@app.route('/event/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
	e = models.Event.query.get(id)
	hit_id = e.hit_id #get the id of the Hit the event corresponds to, as indexed by our db
	form = EventForm()
	if request.method == 'GET':
		form = EventForm(obj=e)
		return render_template('edit_event.html', form = form, event = e, hit_id = hit_id )
	if request.method == 'POST':
		for fieldname, value in form.data.items():
			setattr(e, fieldname, value)
		# print e #sanity test
		db.session.commit()
		'''
		eventData = request.get_json()
		for key in eventData:
			setattr(e, key, eventData[key])
		'''
		dest = '/hits/' + str(hit_id)
		print dest
		return redirect(dest) #no idea why url_for doesn't work here


'''
@app.route('/test')
def test():
	form = EventForm()
	hit = models.Hit.query.get(92)
	return render_template('test.html', form = form, hit= hit, external_submit_url = os.environ['EXTERNAL_SUBMIT_SANDBOX_URL'], hit_id = hit.id)
'''
