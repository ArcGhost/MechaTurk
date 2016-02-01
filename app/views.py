from flask import render_template, flash, redirect, request, g, url_for
from app import app, db, models
from .create_HIT import create_task, mturk
from sqlalchemy import desc
from .forms import TurkForm, CreateHITForm, UsernamePasswordForm, FeedbackForm
from .models import Hit, User
import os, boto.mturk.connection, boto.mturk.question
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager



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
    if h.turk_input:
        entries = [x.split(' | ') for x in h.turk_input.split('\r\n')]
    else:
        entries = ''
    return render_template('view_hit.html', 
                        hit = h,
                        entries = entries, 
                        form = form)


@app.route('/hits/<id>/<judgement>') #routes for approval/rejection of Turk work
@login_required
def approve_or_reject(id, judgement):
    h = models.Hit.query.get(id)
    form = FeedbackForm()
    assignment = mturk.get_assignments(h.hit_id, status='Submitted')[0] #get the first submitted assignment for the hit (this will exclude approved and rejected assignments)
    ass_id = assignment.AssignmentId #fetch the id
    feedback = form.feedback.data #fetch the Tassl feedback
    h.status = judgement
    db.session.commit()
    if judgement == 'approved':
        mturk.approve_assignment(ass_id, feedback)
    elif judgement == 'rejected':
        mturk.reject_assignment(ass_id, feedback)
        #need some kind of success response from Amazon, no?
    return redirect(url_for('all_hits'))


@app.route('/hits/create', methods=['GET', 'POST'])  #page for creating new HITs | needs login for GET and POST
@login_required
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

	
@app.route('/consignment/<id>', methods=['GET', 'POST']) #display page for a particular HIT (POST not allowed until Turk accepts job and worker_id is provided by the get request) | no login required
def hit_consignment(id):
    form = TurkForm()
    h = models.Hit.query.get(id)
    if request.method == 'GET':
    	#get the following variables from Amazon when the GET request originates from there
    	worker_id = request.args.get("workerId")
    	assignment_id = request.args.get("assignmentId")
        task_id = request.args.get("hitId")
    	return render_template('task.html', 
    					id = id,
                        provided_link= h.url,
                        provided_description= h.title,
                        hit_id = task_id,
                        worker_id = worker_id,
                        assignment_id = assignment_id,
                        external_submit_url = os.environ['EXTERNAL_SUBMIT_SANDBOX_URL'],
                        form=form)
    if request.method == 'POST':
    	# need to confer with James and ask how Turk input will be ingested to the Tassl events DB
    	# need to check with field validation here
    	h.turk_input = form.turk_input.data
        # our parsing goes here, or data can just be entered into our db directly; data is sanitized by wtforms when .data is called
        h.status = 'reviewable'
    	db.session.commit()
    	flash('Turk input been recorded.')
    	return 'success'
