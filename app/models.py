from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db
from sqlalchemy.orm import class_mapper, ColumnProperty
import sqlalchemy


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True) #assigned by us
	event_name = db.Column(db.String(128))
	event_type = db.Column(db.String(128))
	host_name = db.Column(db.String(128))
	on_campus = db.Column(db.String(16))
	virtual = db.Column(db.String(16))
	location = db.Column(db.Text())
	description = db.Column(db.Text())
	start_date = db.Column(db.String(128))
	end_date =  db.Column(db.String(128))
	start_time = db.Column(db.String(128))
	end_time = db.Column(db.String(128))
	time_zone = db.Column(db.String(128))
	all_day = db.Column(db.String(16))
	general_pricing = db.Column(db.String(128))
	member_pricing = db.Column(db.String(128))
	non_member_pricing = db.Column(db.String(128))
	registration_req = db.Column(db.String(16))
	registration_url = db.Column(db.Text())
	event_page_url = db.Column(db.Text())
	hit_id = db.Column(db.Integer, db.ForeignKey('hit.id')) #belongs to HIT

	def columns(self):
		#Return the actual columns of a SQLAlchemy-mapped object
		return [prop.key for prop in class_mapper(self.__class__).iterate_properties if isinstance(prop, ColumnProperty)]

	def __repr__(self):
		summary = ''
		for column in self.columns():
			summary = summary + str(column) + ':  ' + '%r \n' % (getattr(self, column))
		return summary



class Hit(db.Model):
	id = db.Column(db.Integer, primary_key=True) #assigned by us
	# the following are required for HIT creation / manipulation
	hit_id = db.Column(db.String(128), index=True, unique=True) #assigned by Amazon	
	title = db.Column(db.String(128)) #description given by Tassl employee
	worker_id = db.Column(db.String(128))  #given when Turk accepts an assignment
	assignment_id = db.Column(db.String(128))  #given when a Turk accepts an assignment
	url = db.Column(db.String(256))  #given by Tassl employee
	status = db.Column(db.String(128)) #open, reviewable, approved, expired, or rejected
	bounty = db.Column(db.String(16))  #given by Tassl employee, reward for task
	instructions = db.Column(db.Text()) #given by Tassl employee, directions to worker
	created_at = db.Column(db.DateTime) #to track staleness
	keywords = db.Column(db.Text()) #given by Tassl employee
	deadline = db.Column(db.Integer) #given by Tassl employee, days to complete assignment
	school = db.Column(db.String(128)) #given by Tassl employee
	# the following are what we want to track
	turk_input = db.Column(db.Text()) #resultant work of the Turk
	events = db.relationship('Event', backref='HIT', lazy='dynamic')

	def __repr__(self):
		return 'ID: %r - %r \n Created at: %r \n Deadline: %r \n HIT #: %r \n status: %r \n link: %r \n bounty: %r \n school: %r\n\n data dump: \n %r \n\n\n' % \
		(self.id, self.title, self.created_at, self.deadline, self.hit_id, self.status, self.url, self.bounty, self.school, self.turk_input)



class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True)
	_password = db.Column(db.String(128))

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self, plaintext):
		return bcrypt.check_password_hash(self._password, plaintext)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def __repr__(self):
		return '<User %r>' % (self.username)