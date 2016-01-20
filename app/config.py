import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
WTF_CSRF_ENABLED = True
SECRET_KEY = 'this-is-the-secret-key-for-wtforms-csrf-protection'