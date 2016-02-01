"""this is a script to add a Human Intelligence Task to MechanicalTurk"""

import boto.mturk.connection
import boto.mturk.question
import os
import datetime


mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
    host = os.environ['SANDBOX_HOST'],
    debug = 1 # debug = 2 prints out all requests. but we'll just keep it at 1
)

#sanity check
#print boto.Version
#print mturk.get_account_balance()

def create_task(id, title, description, keywords):
    URL = "https://tassl-mechaturk.herokuapp.com/consignment/" + str(id)
    frame_height = 500 # the height of the iframe holding the external hit
    amount = .05
    questionform = boto.mturk.question.ExternalQuestion( URL, frame_height )
    create_hit_result = mturk.create_hit(
        title = title,
        description = description,
        keywords = keywords,
        question = questionform,
        lifetime = datetime.timedelta(365), #time an HIT can be searchable, in days
        duration = datetime.timedelta(3), #time an HIT can be worked, once accepted, in days
        reward = boto.mturk.price.Price( amount = amount),
        response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
        )
    HIT = create_hit_result[0]
    assert create_hit_result.status
    return HIT.HITId

def approve_task(id, feedback):
    approve_assignment(assignment_id, feedback=None)
    pass

def reject_task(id, feedback):
    pass












