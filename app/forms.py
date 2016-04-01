from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, TextField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired
from wtforms_components import SelectField, SelectMultipleField
import wtforms_components

class TurkForm(Form):
    turk_input = TextAreaField('turk_input', validators=[DataRequired()])
    
class CreateHITForm(Form):
	title = StringField('title', validators=[DataRequired()])
	url = StringField('url', validators=[DataRequired()])
	instructions = TextAreaField('instructions', validators=[DataRequired()])
	keywords = TextAreaField('keywords', validators=[DataRequired()]) 
	bounty = StringField('bounty', validators=[DataRequired()])
	deadline = StringField('deadline', validators=[DataRequired()])
	school = SelectField(label='school', coerce=int, validators=[DataRequired()])


class EventForm(Form):
	TIMEZONE_CHOICES = [('',''),('Pacific', 'Pacific'), ('Mountain ','Mountain '), ('Central ','Central '), ('Eastern ','Eastern ')]
	YES_NO = [('',''), ('yes','yes'), ('no','no')]
	host_name = SelectField(label='host_name')
	event_name = StringField('event_name')
	event_type = SelectField(label='event_type')
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