#!/Users/alex/.virtualenvs/mechaturk/bin/python
# This script seeds the database with some HITs.

"""
class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hit_id = db.Column(db.String(128), index=True, unique=True) #assigned by Amazon	
    title = db.Column(db.String(128), unique=True) #description given by Tassl employee
    worker_id = db.Column(db.String(128))  #given when Turk accepts an assignment
    url = db.Column(db.String(256))  #given by Tassl employee
    status = db.Column(db.String(128)) #open, in progress, waiting for review, approved, or denied; set by logic
    turk_input = db.Column(db.Text()) #resultant work of the Turk

"""

from app import db, models

#remove previous HITs
hits = models.Hit.query.all()
for h in hits:
	db.session.delete(h)
db.session.commit()

print( "Adding seed-data to the database.")

hit_seeds = [
	{'hit_id': '1234567890', 'title': 'UCLA 2016 Football Schedule', 'worker_id':'','url': 'http://www.fbschedules.com/ncaa-16/2016-ucla-bruins-football-schedule.php', 'status':'open', 'turk_input': ''},
	{'hit_id': '2345678901', 'title': 'Rowan 2016 Baseball Schedule', 'worker_id':'ABCDEFGHIJKL','url': 'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'status':'in progress', 'turk_input': ''},
	{'hit_id': '3456789012', 'title': 'Cornell 2015 Basketball Schedule', 'worker_id':'BCDEFGHIJKLM','url': 'http://www.cornellbigred.com/schedule.aspx?path=mbball', 'status':'approved', 'turk_input': 'Cornell Vs. Colgate University | 11/16/15 | 19:00 | Hamilton, NY \n Cornell Vs. Georgia Tech | 11/13/15 | 20:00 | Atlanta, GA \n Cornell Vs. Binghamton | 11/18/15 | 18:00 | Ithaca, NY \n'}
	]

for x in hit_seeds:
	hit = models.Hit(hit_id=x['hit_id'], title=x['title'], worker_id = x['worker_id'], url=x['url'], status=x['status'], turk_input=x['turk_input'])
	db.session.add(hit)
	db.session.commit()

hits = models.Hit.query.all()
print('Done. DB dump follows:\n')
print('========== HITs ==========')
print(hits)

	

