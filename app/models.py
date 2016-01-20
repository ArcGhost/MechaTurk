from app import db


class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True) #assigned by us
    hit_id = db.Column(db.String(128), index=True, unique=True) #assigned by Amazon	
    title = db.Column(db.String(128), unique=True) #description given by Tassl employee
    worker_id = db.Column(db.String(128))  #given when Turk accepts an assignment
    url = db.Column(db.String(256))  #given by Tassl employee
    status = db.Column(db.String(128)) #open, in progress, waiting for review, approved, or denied; set by logic
    turk_input = db.Column(db.Text()) #resultant work of the Turk

    def __repr__(self):
        return 'ID: %r - %r, HIT #: %r, status: %r, link: %r \n data dump: \n\n %r' % (self.id, self.title, self.hit_id, self.status, self.url, self.turk_input)