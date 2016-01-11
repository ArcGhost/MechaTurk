from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class TurkForm(Form):
    turk_input = TextAreaField('turk_input', validators=[DataRequired()])
    #hidden_assignmentID = HiddenField('hidden_assignmentID')
    #hidden_HITID = HiddenField('hidden_HITID')

class CreateHITForm(Form):
	hit_title = StringField('hit_title', validators=[DataRequired()])
	hit_url = StringField('hit_url', validators=[DataRequired()])
	hit_description = TextAreaField('hit_description', validators=[DataRequired()])
	hit_keywords = TextAreaField('hit_keywords', validators=[DataRequired()]) 
