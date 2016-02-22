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
import datetime

#remove previous HITs
hits = models.Hit.query.all()
for h in hits:
	db.session.delete(h)
db.session.commit()

#add HIT seeds
print( "Adding seed-data to the database.")
dt1 = datetime.datetime.now()
dt2 = datetime.datetime.now() - datetime.timedelta(3)
dt3 = datetime.datetime.now() - datetime.timedelta(1)

hit_seeds = [
	{'hit_id': '1234567890', 'title': 'UCLA 2016 Football Schedule', 'worker_id':'', 'bounty':'4.50', 'url': 'http://www.fbschedules.com/ncaa-16/2016-ucla-bruins-football-schedule.php', 'status':'open', 'turk_input': '', 'created_at': dt1, 'school':'UCLA', 'deadline':3, 'keywords':'Tassl, alumni, UCLA' },
	{'hit_id': '2345678901', 'title': 'Rowan 2016 Baseball Schedule', 'bounty':'7.50', 'worker_id':'ABCDEFGHIJKL','url': 'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'status':'reviewable', 'turk_input': 'Rowan Vs. Randolph-Macon College (DH) | 02/27/2016 | 11:00 | Ashland, VA\r\nRowan Vs. Randolph-Macon College | 02/28/2016 | 11:00 | Ashland, VA\r\nRowan Vs. Stevens Institute of Technology | 03/06/2016 | 12:00 | Glassboro, NJ\r\nRowan Vs. York College (PA) | 03/07/2016 | 15:00 | Glassboro, NJ\r\nRowan Vs. Neumann University | 03/22/2016 | 15:30 | Glassboro, NJ', 'created_at': dt2, 'school':'Rowan', 'deadline':2, 'keywords':'Tassl, alumni, snakes, data collection'},
	{'hit_id': '3456789012', 'title': 'Cornell 2015 Basketball Schedule', 'bounty':'6.50', 'worker_id':'BCDEFGHIJKLM','url': 'http://www.cornellbigred.com/schedule.aspx?path=mbball', 'status':'approved', 'turk_input': 'Cornell Vs. Colgate University | 11/16/15 | 19:00 | Hamilton, NY\r\nCornell Vs. Georgia Tech | 11/13/15 | 20:00 | Atlanta, GA\r\nCornell Vs. Binghamton | 11/18/15 | 18:00 | Ithaca, NY', 'created_at': dt3, 'school':'Cornell', 'deadline':1, 'keywords':'Tassl, alumni, planes, data collection'}
	]

for x in hit_seeds:
	hit = models.Hit(hit_id=x['hit_id'], title=x['title'], worker_id = x['worker_id'], url=x['url'], status=x['status'], turk_input=x['turk_input'], bounty=x['bounty'], created_at=x['created_at'], school=x['school'], deadline=x['deadline'], keywords=x['keywords'])
	db.session.add(hit)
	db.session.commit()

#add admin seed
admins = models.User.query.all()
for a in admins:
	db.session.delete(a)
db.session.commit()
admin = models.User()
admin.username = 'falken'
admin.password = 'joshua'
db.session.add(admin)
db.session.commit()



hits = models.Hit.query.all()
print('Done. DB dump follows:\n')
print('========== HITs ==========')
print(hits)
print('Professor Falken is admin.')

	

