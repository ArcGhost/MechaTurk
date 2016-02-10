from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db

class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True) #assigned by us
    hit_id = db.Column(db.String(128), index=True, unique=True) #assigned by Amazon	
    title = db.Column(db.String(128)) #description given by Tassl employee
    worker_id = db.Column(db.String(128))  #given when Turk accepts an assignment
    assignment_id = db.Column(db.String(128))  #given when a Turk accepts an assignment
    url = db.Column(db.String(256))  #given by Tassl employee
    status = db.Column(db.String(128)) #open, reviewable, approved, or rejected
    turk_input = db.Column(db.Text()) #resultant work of the Turk
    bounty = db.Column(db.String(16))  #given by Tassl employee, reward for task
    instructions = db.Column(db.Text()) #given by Tassl employee, directions to worker
    created_at = db.Column(db.DateTime) #to track staleness
    keywords = db.Column(db.Text()) #given by Tassl employee

    def __repr__(self):
        return 'ID: %r - %r \n Created at: %r \n HIT #: %r \n status: %r \n link: %r \n bounty: %r \n\n data dump: \n %r \n\n\n' % \
        (self.id, self.title, self.created_at, self.hit_id, self.status, self.url, self.bounty, self.turk_input)



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