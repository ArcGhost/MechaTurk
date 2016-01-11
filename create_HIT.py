#!/Users/alex/.virtualenvs/mechaturk/bin/python
"""this is a script to add a Human Intelligence Task to MechanicalTurk"""

import boto.mturk.connection
import boto.mturk.question

sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
real_host = 'mechanicalturk.amazonaws.com'

mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = 'AKIAIDJVQDQQ53LMFLFQ',
    aws_secret_access_key = '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',
    host = sandbox_host,
    debug = 1 # debug = 2 prints out all requests. but we'll just keep it at 1
)

print boto.Version
print mturk.get_account_balance()


URL = "https://rocky-journey-7052.herokuapp.com/"
title = "Alex's Custom External HIT!" # Enter the name of the HIT. Be specific. 
description = "Are you suggesting that coconuts migrate? It can grip it by the husk." #Describe the HIT. The search mechanism searches using this description so use words that you think will help Workers find your HITs
keywords = ["cats", "dogs", "rabbits"] # comma-separated list of words that Workers can use to find your HIT
frame_height = 500 # the height of the iframe holding the external hit
amount = .05


questionform = boto.mturk.question.ExternalQuestion( URL, frame_height )

create_hit_result = mturk.create_hit(
    title = title,
    description = description,
    keywords = keywords,
    question = questionform,
    reward = boto.mturk.price.Price( amount = amount),
    response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
    )

HIT = create_hit_result[0]
assert create_hit_result.status

print '[create_hit( %s, $%s ): %s]' % ( URL, amount, HIT.HITId )