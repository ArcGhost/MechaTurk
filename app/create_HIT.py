"""This module will add a Human Intelligence Task to MechanicalTurk"""

import boto.mturk.connection
import boto.mturk.question
import os

mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
    host = os.environ['SANDBOX_HOST'],
    debug = 1 # debug = 2 prints out all requests. but we'll just keep it at 1
)

def create_HIT(title, description, keywords, id):
    #this function creates an HIT with a Tassl-provided title, description, and keywords
    #the API-call also requres a frame height, a bounty, and a url for the hosted question, which are all hardcoded here in this script

    URL = "https://sheltered-reef-1374.herokuapp.com/hits/" + str(id)
    frame_height = 500 # the height of the iframe holding the external hit
    amount = .05 #amount paid for the task
    question_form = boto.mturk.question.ExternalQuestion( URL, frame_height )

    create_hit_result = mturk.create_hit(title, description, keywords, question = question_form,
        reward = boto.mturk.price.Price(amount = amount),
        response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
        )

    HIT = create_hit_result[0]
    assert create_hit_result.status
    return HIT.HITId

    #print '[create_hit( %s, $%s ): %s]' % ( URL, amount, HIT.HITId )


