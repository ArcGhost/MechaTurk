from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, TextField, PasswordField, SelectField
from wtforms.validators import DataRequired

class TurkForm(Form):
    turk_input = TextAreaField('turk_input', validators=[DataRequired()])
    
class CreateHITForm(Form):
	title = StringField('title', validators=[DataRequired()])
	url = StringField('url', validators=[DataRequired()])
	instructions = TextAreaField('instructions', validators=[DataRequired()])
	keywords = TextAreaField('keywords', validators=[DataRequired()]) 
	bounty = StringField('bounty', validators=[DataRequired()])
	deadline = StringField('deadline', validators=[DataRequired()])
	school = StringField('bounty', validators=[DataRequired()])

class EventForm(Form):
	TIMEZONE_CHOICES = [('',''),('Pacific Standard Time', 'Pacific Standard Time'), ('Mountain Standard Time','Mountain Standard Time'), ('Central Standard Time','Central Standard Time'), ('Eastern Standard Time','Eastern Standard Time')]
	YES_NO = [('',''), ('yes','yes'), ('no','no')]
	EVENT_TYPES = [('',''),('Banquet/Reception', 'Banquet/Reception'), ('Conference/Workshop/Forum', 'Conference/Workshop/Forum'), ('Cultural', 'Cultural'), ('For A Cause', 'For A Cause'), ('Game Watch', 'Game Watch'), ('Homecoming', 'Homecoming'), ('Just for Fun', 'Just for Fun'), ('Leadership Meeting', 'Leadership Meeting'), ('Networking', 'Networking'), ('Other', 'Other'), ('Professional Development', 'Professional Development'), ('Reunion', 'Reunion'), ('Service/Philanthropy', 'Service/Philanthropy'), ('Sports', 'Sports'), ('Tailgate', 'Tailgate'), ('Volunteer Opportunities', 'Volunteer Opportunities'), ('Webinar', 'Webinar')]
	host_name = StringField('host_name')
	event_name = StringField('event_name')
	event_type = SelectField(label='event_type', choices=EVENT_TYPES)
	on_campus = SelectField(label='on_campus', choices=YES_NO)
	virtual = SelectField(label='virtual', choices=YES_NO)
	location = StringField('location')
	description = TextAreaField('description')
	start_date = StringField('start_date')
	end_date =  StringField('end_date')
	start_time = StringField('start_time')
	end_time = StringField('end_time')
	time_zone = SelectField(label='time_zone', choices=TIMEZONE_CHOICES)
	all_day = SelectField(label='all_day', choices=YES_NO)
	general_pricing = StringField('general_pricing')
	member_pricing = StringField('member_pricing')
	non_member_pricing = StringField('non_member_pricing')
	registration_req = SelectField(label='registration_req', choices=YES_NO)
	registration_url = StringField('registration_url')
	event_page_url = StringField('event_page_url')	



class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FeedbackForm(Form):
	feedback = TextAreaField('task_feedback')