from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
#app.config.from_object('config')
app.config['DEBUG'] = True #need this to see error tracing
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import views, models

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "index"

from .models import User
@login_manager.user_loader
def load_user(userid):
    return models.User.query.filter(User.id==userid).first()

