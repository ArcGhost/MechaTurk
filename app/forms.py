from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, TextField, PasswordField
from wtforms.validators import DataRequired

class TurkForm(Form):
    turk_input = TextAreaField('turk_input', validators=[DataRequired()])
    

class CreateHITForm(Form):
	hit_title = StringField('hit_title', validators=[DataRequired()])
	hit_url = StringField('hit_url', validators=[DataRequired()])
	hit_description = TextAreaField('hit_description', validators=[DataRequired()])
	hit_keywords = TextAreaField('hit_keywords', validators=[DataRequired()]) 


class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])