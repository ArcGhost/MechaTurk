#this file contains all functions for fetching data from Tassl-Connect
#as well as functions for massaging data before sending it over to Tassl-Connect

import requests
import json
from rfc3339 import rfc3339
from datetime import datetime
from app import app, db, models


def get_host_choices(school_id=319): #get hosts for an event, given a school id

	si = str(school_id)
	OPTGROUP_DEPARTMENT = 0
	OPTGROUP_COLLEGE = 1
	OPTGROUP_SCHOOL_GROUP = 2

	host_choices = []
	host_dict = {}

	a = requests.get('https://api.tasslapp.com/v1/schools/'+si+'/groups')
	b = requests.get('https://api.tasslapp.com/v1/schools/'+si+'/departments')
	c = requests.get('https://api.tasslapp.com/v1/schools/'+si+'/colleges')

	if a.status_code == 200:
		x = []
		for sg in a.json():
			x.append(('%d_%d' % (OPTGROUP_SCHOOL_GROUP, sg['id']), sg['name']))
			host_dict['%d_%d' % (OPTGROUP_SCHOOL_GROUP, sg['id'])] = sg['name']
		if len(x) > 0:
			host_choices.append(('School Group', x))
	if b.status_code == 200:
		y = []
		for dept in b.json():
			y.append(('%d_%d' % (OPTGROUP_DEPARTMENT, dept['id']), dept['name']))
			host_dict['%d_%d' % (OPTGROUP_DEPARTMENT, dept['id'])] = dept['name']
		if len(y) > 0:
			host_choices.append(('Department', y))
	if c.status_code == 200:
		z = []
		for college in c.json():
			z.append(('%d_%d' % (OPTGROUP_COLLEGE, college['id']), college['name']))
			host_dict['%d_%d' % (OPTGROUP_COLLEGE, college['id'])] = college['name']
		if len(z) > 0:
			host_choices.append(('College', z))		

	return host_choices, host_dict



def get_school_choices(): #get list of schools
	SCHOOL_CHOICES = []
	schools_dict = {}
	r = requests.get('https://api.tasslapp.com/v1/schools')
	if r.status_code == 200:
		for x in r.json():
	 		SCHOOL_CHOICES.append((x['id'], x['name']))
	 		schools_dict[x['id']] = x['name']
	return SCHOOL_CHOICES, schools_dict


def get_event_types():
	event_type_choices = []
	event_type_dict = {}
	r = requests.get('https://api.tasslapp.com/v1/events/types')
	if r.status_code == 200:
		for x in r.json():
			event_type_choices.append((x['id'], x['name']))
	 		event_type_dict[x['id']] = x['name']
	return event_type_choices, event_type_dict




def package_event(mt_event):
	event = {}
	event['name'] = str(mt_event.event_name)
	event['start_date'] = rfc3339(datetime.strptime(mt_event.start_date, "%Y-%m-%d"), use_system_timezone=False)
	event['start_time'] = rfc3339(datetime.strptime(mt_event.start_date + " " + mt_event.start_time
		, "%Y-%m-%d %H:%M"), use_system_timezone=False)
	event['end_date'] = rfc3339(datetime.strptime(mt_event.end_date, "%Y-%m-%d"), use_system_timezone=False)
	event['end_time'] = rfc3339(datetime.strptime(mt_event.end_date + " " + mt_event.end_time
		, "%Y-%m-%d %H:%M"), use_system_timezone=False)
	event['all_day'] = True if (mt_event.all_day == 'yes') else False
	event['description'] = str(mt_event.description)
	event['registration_required'] = True if (mt_event.registration_req == 'yes') else False
	event['on_campus'] = True if (mt_event.on_campus == 'yes') else False
	event['registration_url'] = str(mt_event.registration_url)
	event['url'] = str(mt_event.event_page_url)
	event['virtual'] = True if (mt_event.virtual == 'yes') else False
	event['time_zone'] = str(mt_event.time_zone)
	event['google_location_id'] = str(mt_event.google_location_id)
	event['event_type_id'] = mt_event.event_type

	if bool(mt_event.general_pricing):
		event['general_cost'] = float(mt_event.general_pricing)  
	if bool(mt_event.member_pricing):
		event['member_cost'] = float(mt_event.general_pricing) 
	if bool(mt_event.non_member_pricing):
		event['non_member_cost'] = float(mt_event.non_member_pricing) 

	x, hosts_dict = get_host_choices()
	event['host_name'] = str(hosts_dict[mt_event.host_name])

	host = mt_event.host_name.split("_")
	if host[0] == "0":
		event['department_id'] = int(host[1])
	elif host[0] == "1":
		event['college_id'] = int(host[1])
	elif host[0] == "2":
		event['school_group_id'] = int(host[1])

	h = models.Hit.query.get(mt_event.hit_id)
	event['school_id'] = h.school

	return json.dumps(event)

'''
#lifted from Tassl-Connect models.py

class EventBase(FlexibleModel):
x    name = StringType()
x    start_date = DateTimeType()
x    start_time = DateTimeType()
x    end_date = DateTimeType()
x    end_time = DateTimeType()
x    all_day = BooleanType()
x    description = StringType()
x    event_type_id = IntType()
x    registration_required = BooleanType()
x    registration_url = StringType()
x    on_campus = BooleanType()
x    host_name = StringType()
x    url = StringType()
x    school_id = IntType()
x    college_id = IntType()
x    school_group_id = IntType()
x    google_location_id = StringType()
x    virtual = BooleanType()
x    time_zone = StringType()
x    department_id = IntType()
x    general_cost = FloatType()
x    member_cost = FloatType()
x    non_member_cost = FloatType()
    



'''	