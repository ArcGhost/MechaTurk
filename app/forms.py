from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, TextField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired

class TurkForm(Form):
    turk_input = TextAreaField('turk_input', validators=[DataRequired()])
    
class CreateHITForm(Form):
	hit_title = StringField('hit_title', validators=[DataRequired()])
	hit_url = StringField('hit_url', validators=[DataRequired()])
	hit_instructions = TextAreaField('hit_instructions', validators=[DataRequired()])
	hit_keywords = TextAreaField('hit_keywords', validators=[DataRequired()]) 
	hit_bounty = StringField('hit_bounty', validators=[DataRequired()])
	hit_deadline = StringField('hit_deadline', validators=[DataRequired()])
	hit_school = StringField('hit_bounty', validators=[DataRequired()])

class EventForm(Form):
	TIMEZONE_CHOICES = [('PST', 'Pacific Standard Time'), ('MST','Mountain Standard Time'), ('CST','Central Standard Time'), ('EST','Eastern Standard Time')]
	event_host_name = StringField('event_host_name')
	event_name = StringField('event_name')
	event_type = StringField('event_type')
	event_on_campus = RadioField('event_on_campus', choices=[('True','Yes'),('False','No')])
	event_virtual = RadioField('event_virtual', choices=[('True','Yes'),('False','No')])
	event_location = StringField('event_location')
	event_description = TextAreaField('event_description')
	event_start_date = StringField('event_start_date')
	event_end_date =  StringField('event_end_date')
	event_start_time = StringField('event_start_time')
	event_end_time = StringField('event_end_time')
	event_time_zone = SelectField(label='event_time_zone', choices=TIMEZONE_CHOICES)
	event_all_day = RadioField('event_all_day', choices=[('True','Yes'),('False','No')])
	event_general_pricing = StringField('event_general_pricing')
	event_member_pricing = StringField('event_member_pricing')
	event_non_member_pricing = StringField('event_non_member_pricing')
	event_registration_req = RadioField('event_registration_req', choices=[('True','Yes'),('False','No')])
	event_registration_url = StringField('event_registration_url')
	event_page_url = StringField('event_page_url')	



class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FeedbackForm(Form):
	feedback = TextAreaField('task_feedback')