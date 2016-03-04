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
    instructions = db.Column(db.Text()) #instructions to the Turk
"""

from app import db, models
import datetime
from sqlalchemy import desc

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
	{'hit_id': '1234567890', 'title': 'UCLA 2016 Football Schedule', 'worker_id':'', 'bounty':'4.50', 'url': 'http://www.fbschedules.com/ncaa-16/2016-ucla-bruins-football-schedule.php', 'status':'open', 'created_at': dt1, 'school':'UCLA', 'deadline':3, 'keywords':'Tassl, alumni, UCLA', 'instructions':'Enter all event info relating to 2016 season.' },
	{'hit_id': '2345678901', 'title': 'Rowan 2016 Baseball Schedule', 'bounty':'7.50', 'worker_id':'ABCDEFGHIJKL','url': 'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'status':'reviewable', 'created_at': dt2, 'school':'Rowan', 'deadline':2, 'keywords':'Tassl, alumni, snakes, data collection', 'instructions':'Enter all event info relating to the RussMatt Central Florida Invitational'},
	{'hit_id': '3456789012', 'title': 'Cornell 2015 Basketball Schedule', 'bounty':'6.50', 'worker_id':'BCDEFGHIJKLM','url': 'http://www.cornellbigred.com/schedule.aspx?path=mbball', 'status':'approved', 'created_at': dt3, 'school':'Cornell', 'deadline':1, 'keywords':'Tassl, alumni, planes, data collection', 'instructions':'Enter all event info relating to the 2015 season.'}
	]

for x in hit_seeds:
	hit = models.Hit(hit_id=x['hit_id'], title=x['title'], worker_id = x['worker_id'], url=x['url'], status=x['status'], bounty=x['bounty'], created_at=x['created_at'], school=x['school'], deadline=x['deadline'], keywords=x['keywords'], instructions=x['instructions'])
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






#remove all existing events
events = models.Event.query.all()
for e in events:
	db.session.delete(e)
db.session.commit()

#add event seeds
hits = models.Hit.query.all()
h = hits[-2]

event_seeds = [ {'event_type':'Game Watch', 'event_name':'Rowan Vs Endicott College', 'host_name':'Central Florida University', 'on_campus':'yes', 'virtual':'no', 'location':'Henley Field, Lakeland, FL', 'description':'This is the event description for the game.', 'start_date':'3/18/2016', 'end_date':'3/19/2016', 'start_time':'11:00am', 'end_time':'1:30pm', 'time_zone':'Eastern Standard Time', 'all_day':'no', 'general_pricing':'$5.00', 'member_pricing':'$3.00', 'non_member_pricing':'$5.00', 'registration_req':'no', 'registration_url':'', 'event_page_url':'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'hit_id':h.id} , 
	{'event_type':'Game Watch', 'event_name':'Rowan Vs Wheaton College', 'host_name':'Central Florida University', 'on_campus':'yes', 'virtual':'no', 'location':'Lake Myrtle Park Field 7, Auburndale, FL', 'description':'This is the event description for the game.', 'start_date':'3/19/2016', 'end_date':'3/19/2016', 'start_time':'10:30am', 'end_time':'1:00pm', 'time_zone':'Eastern Standard Time', 'all_day':'no', 'general_pricing':'$5.00', 'member_pricing':'$3.00', 'non_member_pricing':'$5.00', 'registration_req':'no', 'registration_url':'', 'event_page_url':'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'hit_id':h.id}, 
	{'event_type':'Game Watch', 'event_name':'Rowan Vs Gudger College', 'host_name':'CFU', 'on_campus':'yes', 'virtual':'no', 'location':'2345 Sesame St.', 'description':'This is the event description for the game.', 'start_date':'3/19/2016', 'end_date':'3/19/2016', 'start_time':'10:30am', 'end_time':'1:00pm', 'time_zone':'Eastern Standard Time', 'all_day':'no', 'general_pricing':'$5.00', 'member_pricing':'$3.00', 'non_member_pricing':'$5.00', 'registration_req':'no', 'registration_url':'', 'event_page_url':'http://www.rowanathletics.com/schedule.aspx?path=baseball', 'hit_id':h.id}]

for x in event_seeds:
	event = models.Event(event_type=x['event_type'], event_name=x['event_name'], host_name=x['host_name'], on_campus=x['on_campus'], virtual=x['virtual'], location=x['location'], description=x['description'], start_date=x['start_date'], end_date=x['end_date'], start_time=x['start_time'], end_time=x['end_date'], time_zone=x['time_zone'], all_day=x['all_day'], general_pricing=x['general_pricing'], member_pricing=x['member_pricing'], non_member_pricing=x['non_member_pricing'], registration_req=x['registration_req'], registration_url=x['registration_url'], event_page_url=x['event_page_url'], hit_id=x['hit_id'])
	db.session.add(event)
	db.session.commit()	













hits = models.Hit.query.all()
print('Done. DB dump follows:\n')
print('========== HITs ==========')
print(hits)
print('Professor Falken is admin.')

	

