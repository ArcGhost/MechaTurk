from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, TextField, PasswordField, SelectField
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
	TIMEZONE_CHOICES = [('',''),('Pacific Standard Time', 'Pacific Standard Time'), ('Mountain Standard Time','Mountain Standard Time'), ('Central Standard Time','Central Standard Time'), ('Eastern Standard Time','Eastern Standard Time')]
	YES_NO = [('',''), ('Yes','Yes'), ('No','No')]
	EVENT_TYPES = [('',''),('Banquet/Reception', 'Banquet/Reception'), ('Conference/Workshop/Forum', 'Conference/Workshop/Forum'), ('Cultural', 'Cultural'), ('For A Cause', 'For A Cause'), ('Game Watch', 'Game Watch'), ('Homecoming', 'Homecoming'), ('Just for Fun', 'Just for Fun'), ('Leadership Meeting', 'Leadership Meeting'), ('Networking', 'Networking'), ('Other', 'Other'), ('Professional Development', 'Professional Development'), ('Reunion', 'Reunion'), ('Service/Philanthropy', 'Service/Philanthropy'), ('Sports', 'Sports'), ('Tailgate', 'Tailgate'), ('Volunteer Opportunities', 'Volunteer Opportunities'), ('Webinar', 'Webinar')]
	event_host_name = StringField('event_host_name')
	event_name = StringField('event_name')
	event_type = SelectField(label='event_type', choices=EVENT_TYPES)
	event_on_campus = SelectField(label='event_on_campus', choices=YES_NO)
	event_virtual = SelectField(label='event_virtual', choices=YES_NO)
	event_location = StringField('event_location')
	event_description = TextAreaField('event_description')
	event_start_date = StringField('event_start_date')
	event_end_date =  StringField('event_end_date')
	event_start_time = StringField('event_start_time')
	event_end_time = StringField('event_end_time')
	event_time_zone = SelectField(label='event_time_zone', choices=TIMEZONE_CHOICES)
	event_all_day = SelectField(label='event_all_day', choices=YES_NO)
	event_general_pricing = StringField('event_general_pricing')
	event_member_pricing = StringField('event_member_pricing')
	event_non_member_pricing = StringField('event_non_member_pricing')
	event_registration_req = SelectField(label='event_registration_req', choices=YES_NO)
	event_registration_url = StringField('event_registration_url')
	event_page_url = StringField('event_page_url')	



class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FeedbackForm(Form):
	feedback = TextAreaField('task_feedback')